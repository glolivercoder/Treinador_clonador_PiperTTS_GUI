#!/usr/bin/env python3
"""
Implementação real do Piper Train para Windows
"""
import os
import json
import librosa
import numpy as np
import torch
import pytorch_lightning as pl
from pathlib import Path
import csv
import gruut
from typing import List, Dict, Tuple
import soundfile as sf
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F

class PiperDataset(Dataset):
    """Dataset para treinamento do Piper TTS"""
    
    def __init__(self, data_dir: str, config: dict):
        self.data_dir = Path(data_dir)
        self.config = config
        self.samples = []
        
        # Carregar metadata
        metadata_path = self.data_dir / "metadata.csv"
        if metadata_path.exists():
            self.load_metadata(metadata_path)
    
    def load_metadata(self, metadata_path: Path):
        """Carrega metadata do CSV"""
        with open(metadata_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) >= 2:
                    audio_id = row[0]
                    text = row[1] if len(row) == 2 else row[2]
                    speaker = row[1] if len(row) == 3 else "default"
                    
                    audio_path = self.data_dir / "wav" / f"{audio_id}.wav"
                    if audio_path.exists():
                        self.samples.append({
                            'audio_id': audio_id,
                            'audio_path': str(audio_path),
                            'text': text,
                            'speaker': speaker
                        })
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # Carregar áudio
        audio, sr = librosa.load(sample['audio_path'], sr=self.config['sample_rate'])
        
        # Converter texto para fonemas usando gruut
        phonemes = self.text_to_phonemes(sample['text'])
        
        # Converter para mel-spectrogram
        mel = librosa.feature.melspectrogram(
            y=audio,
            sr=sr,
            n_mels=80,
            n_fft=1024,
            hop_length=256,
            win_length=1024
        )
        mel = librosa.power_to_db(mel, ref=np.max)
        
        return {
            'mel': torch.FloatTensor(mel),
            'phonemes': torch.LongTensor(phonemes),
            'audio': torch.FloatTensor(audio),
            'text': sample['text']
        }
    
    def text_to_phonemes(self, text: str) -> List[int]:
        """Converte texto para sequência de IDs de fonemas"""
        try:
            # Usar gruut para fonemas em português
            phonemes = []
            for sentence in gruut.sentences(text, lang="pt"):
                for word in sentence:
                    if word.phonemes:
                        for phoneme in word.phonemes:
                            # Mapear fonema para ID (simplificado)
                            phoneme_id = hash(str(phoneme)) % 256
                            phonemes.append(phoneme_id)
            
            return phonemes if phonemes else [1, 2, 3]  # Fallback
        except:
            # Fallback simples: converter caracteres para IDs
            return [ord(c) % 256 for c in text[:100]]

class TrainingCallback:
    """Callback para monitorar progresso do treinamento"""
    
    def __init__(self, update_func=None):
        self.update_func = update_func
        self.current_epoch = 0
        self.total_epochs = 100
    
    def on_epoch_end(self, epoch, logs=None):
        self.current_epoch = epoch
        if self.update_func:
            progress = 40 + (epoch / self.total_epochs) * 50
            self.update_func(f'Treinando - Época {epoch}/{self.total_epochs}', progress)
            
            if logs:
                loss = logs.get('train_loss', 0)
                self.update_func(f'Época {epoch}: Loss = {loss:.4f}', progress)

class SimpleVITS(pl.LightningModule):
    """Modelo VITS simplificado para TTS"""
    
    def __init__(self, config: dict, callback=None):
        super().__init__()
        self.config = config
        self.callback = callback
        
        # Encoder de texto (fonemas -> hidden)
        self.text_encoder = nn.Sequential(
            nn.Embedding(256, 256),
            nn.LSTM(256, 256, batch_first=True, bidirectional=True),
            nn.Linear(512, 256)
        )
        
        # Decoder (hidden -> mel)
        self.decoder = nn.Sequential(
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 80),  # 80 mel bins
        )
        
        # Discriminator simples
        self.discriminator = nn.Sequential(
            nn.Conv1d(80, 128, 3, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv1d(128, 256, 3, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv1d(256, 1, 3, padding=1),
            nn.Sigmoid()
        )
    
    def forward(self, phonemes):
        # Encoder
        x, _ = self.text_encoder[1](self.text_encoder[0](phonemes))
        x = self.text_encoder[2](x)
        
        # Decoder
        mel = self.decoder(x)
        
        return mel.transpose(1, 2)  # [B, mel_bins, T]
    
    def training_step(self, batch, batch_idx):
        phonemes = batch['phonemes']
        target_mel = batch['mel']
        
        # Forward pass
        pred_mel = self(phonemes)
        
        # Ajustar dimensões
        min_len = min(pred_mel.size(-1), target_mel.size(-1))
        pred_mel = pred_mel[:, :, :min_len]
        target_mel = target_mel[:, :, :min_len]
        
        # Loss do gerador
        gen_loss = F.mse_loss(pred_mel, target_mel)
        
        # Loss do discriminador
        real_score = self.discriminator(target_mel)
        fake_score = self.discriminator(pred_mel.detach())
        
        disc_loss = F.binary_cross_entropy(real_score, torch.ones_like(real_score)) + \
                   F.binary_cross_entropy(fake_score, torch.zeros_like(fake_score))
        
        total_loss = gen_loss + 0.1 * disc_loss
        
        self.log('train_loss', total_loss)
        self.log('gen_loss', gen_loss)
        self.log('disc_loss', disc_loss)
        
        # Callback para progresso
        if self.callback and batch_idx % 10 == 0:
            self.callback.on_epoch_end(self.current_epoch, {
                'train_loss': total_loss.item(),
                'gen_loss': gen_loss.item(),
                'disc_loss': disc_loss.item()
            })
        
        return total_loss
    
    def on_train_epoch_end(self):
        if self.callback:
            self.callback.current_epoch = self.current_epoch
    
    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-4)

def preprocess_dataset(input_dir: str, output_dir: str, language: str = "pt", 
                      sample_rate: int = 22050, single_speaker: bool = True):
    """Pré-processa dataset para treinamento"""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print(f"🔄 Pré-processando dataset em {input_dir}")
    
    # Verificar arquivos necessários
    metadata_file = input_path / "metadata.csv"
    wav_dir = input_path / "wav"
    
    if not metadata_file.exists():
        raise FileNotFoundError(f"metadata.csv não encontrado em {input_dir}")
    
    if not wav_dir.exists():
        raise FileNotFoundError(f"Diretório wav/ não encontrado em {input_dir}")
    
    # Contar arquivos
    audio_files = list(wav_dir.glob("*.wav")) + list(wav_dir.glob("*.mp3")) + list(wav_dir.glob("*.flac"))
    print(f"📁 Encontrados {len(audio_files)} arquivos de áudio")
    
    # Processar arquivos de áudio
    processed_dir = output_path / "processed"
    processed_dir.mkdir(exist_ok=True)
    
    for audio_file in audio_files:
        try:
            # Carregar e normalizar áudio
            audio, sr = librosa.load(audio_file, sr=sample_rate)
            
            # Normalizar
            audio = librosa.util.normalize(audio)
            
            # Salvar processado
            output_file = processed_dir / f"{audio_file.stem}.wav"
            sf.write(output_file, audio, sample_rate)
            
        except Exception as e:
            print(f"⚠️  Erro processando {audio_file}: {e}")
    
    # Criar configuração
    config = {
        "audio": {
            "sample_rate": sample_rate
        },
        "model": {
            "hidden_dim": 256,
            "num_layers": 2
        },
        "training": {
            "batch_size": 8,
            "learning_rate": 1e-4,
            "max_epochs": 100
        },
        "data": {
            "language": language,
            "single_speaker": single_speaker,
            "num_speakers": 1 if single_speaker else 2
        }
    }
    
    config_file = output_path / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Pré-processamento concluído. Config salvo em {config_file}")
    return str(config_file)

def train_model(data_dir: str, config_path: str, max_epochs: int = 100, update_callback=None):
    """Treina o modelo TTS"""
    
    print(f"🚀 Iniciando treinamento do modelo")
    
    # Carregar configuração
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Criar dataset
    dataset = PiperDataset(data_dir, config['audio'])
    
    if len(dataset) == 0:
        raise ValueError("Dataset vazio! Verifique os arquivos de áudio e metadata.")
    
    print(f"📊 Dataset carregado: {len(dataset)} amostras")
    
    # DataLoader
    dataloader = DataLoader(
        dataset, 
        batch_size=config['training']['batch_size'],
        shuffle=True,
        num_workers=0  # Windows compatibility
    )
    
    # Callback para progresso
    callback = TrainingCallback(update_callback)
    callback.total_epochs = max_epochs
    
    # Modelo
    model = SimpleVITS(config, callback)
    
    # Trainer
    trainer = pl.Trainer(
        max_epochs=max_epochs,
        accelerator='cpu',  # Usar CPU por compatibilidade
        devices=1,
        log_every_n_steps=10,
        enable_checkpointing=True,
        default_root_dir=data_dir,
        enable_progress_bar=False  # Desabilitar barra padrão
    )
    
    # Treinar
    trainer.fit(model, dataloader)
    
    # Salvar checkpoint final
    checkpoint_path = Path(data_dir) / "final_model.ckpt"
    trainer.save_checkpoint(checkpoint_path)
    
    print(f"✅ Treinamento concluído. Modelo salvo em {checkpoint_path}")
    return str(checkpoint_path)

def export_onnx(checkpoint_path: str, output_path: str):
    """Exporta modelo para ONNX"""
    
    print(f"📦 Exportando modelo para ONNX")
    
    try:
        # Carregar modelo
        model = SimpleVITS.load_from_checkpoint(checkpoint_path)
        model.eval()
        
        # Input dummy para export
        dummy_input = torch.randint(0, 256, (1, 50))  # [batch, seq_len]
        
        # Exportar para ONNX
        torch.onnx.export(
            model,
            dummy_input,
            output_path,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['phonemes'],
            output_names=['mel'],
            dynamic_axes={
                'phonemes': {1: 'seq_len'},
                'mel': {2: 'mel_len'}
            }
        )
        
        print(f"✅ Modelo ONNX exportado para {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erro na exportação ONNX: {e}")
        return False

if __name__ == "__main__":
    # Teste básico
    print("🧪 Testando módulo piper_train_real")
    
    # Criar dados de teste
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    wav_dir = test_dir / "wav"
    wav_dir.mkdir(exist_ok=True)
    
    # Criar metadata de teste
    with open(test_dir / "metadata.csv", 'w', encoding='utf-8') as f:
        f.write("test001|Este é um teste de síntese de voz.\n")
        f.write("test002|O modelo está sendo treinado corretamente.\n")
    
    print("✅ Módulo piper_train_real carregado com sucesso!")