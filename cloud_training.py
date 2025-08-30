#!/usr/bin/env python3
"""
Sistema de integração com plataformas de GPU em nuvem para treinamento Piper TTS
"""
import os
import json
import zipfile
import requests
import time
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import tempfile
import shutil

class CloudTrainingManager:
    """Gerenciador de treinamento em nuvem"""
    
    def __init__(self):
        self.supported_platforms = {
            'colab': 'Google Colab',
            'kaggle': 'Kaggle Notebooks', 
            'codesphere': 'CodeSphere'
        }
        self.export_folder = Path("cloud_exports")
        self.export_folder.mkdir(exist_ok=True)
    
    def create_training_package(self, model_name: str, model_dir: str, 
                              platform: str = 'colab') -> str:
        """Cria pacote de treinamento para plataforma específica"""
        
        print(f"📦 Criando pacote de treinamento para {platform}...")
        
        # Criar diretório temporário
        package_dir = self.export_folder / f"{model_name}_{platform}_package"
        package_dir.mkdir(exist_ok=True)
        
        # Copiar dados do modelo
        model_path = Path(model_dir)
        if not model_path.exists():
            raise FileNotFoundError(f"Diretório do modelo não encontrado: {model_dir}")
        
        # Estrutura do pacote
        data_dir = package_dir / "data"
        scripts_dir = package_dir / "scripts"
        config_dir = package_dir / "config"
        
        for dir_path in [data_dir, scripts_dir, config_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Copiar arquivos de dados
        if (model_path / "wav").exists():
            shutil.copytree(model_path / "wav", data_dir / "wav")
        
        if (model_path / "metadata.csv").exists():
            shutil.copy2(model_path / "metadata.csv", data_dir / "metadata.csv")
        
        # Criar scripts específicos da plataforma
        if platform == 'colab':
            self._create_colab_notebook(model_name, scripts_dir, config_dir)
        elif platform == 'kaggle':
            self._create_kaggle_notebook(model_name, scripts_dir, config_dir)
        elif platform == 'codesphere':
            self._create_codesphere_config(model_name, scripts_dir, config_dir)
        
        # Criar arquivo ZIP
        zip_path = self.export_folder / f"{model_name}_{platform}_training.zip"
        self._create_zip_package(package_dir, zip_path)
        
        # Limpar diretório temporário
        shutil.rmtree(package_dir)
        
        print(f"✅ Pacote criado: {zip_path}")
        return str(zip_path)
    
    def _create_colab_notebook(self, model_name: str, scripts_dir: Path, config_dir: Path):
        """Cria notebook do Google Colab"""
        
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        f"# 🎤 Treinamento Piper TTS - {model_name}\n",
                        "\n",
                        "Este notebook treina um modelo de voz personalizado usando Piper TTS no Google Colab.\n",
                        "\n",
                        "## 📋 Instruções:\n",
                        "1. Execute todas as células em ordem\n",
                        "2. Aguarde o treinamento completar\n",
                        "3. Baixe os modelos gerados\n"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# 🔧 Configuração do ambiente\n",
                        "!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118\n",
                        "!pip install pytorch-lightning>=1.8.0\n",
                        "!pip install librosa>=0.9.2\n",
                        "!pip install soundfile scipy\n",
                        "!pip install onnxruntime-gpu\n",
                        "!pip install gruut>=2.0.0\n",
                        "!pip install tensorboard\n",
                        "\n",
                        "import torch\n",
                        "print(f'🚀 GPU disponível: {torch.cuda.is_available()}')\n",
                        "if torch.cuda.is_available():\n",
                        "    print(f'📱 GPU: {torch.cuda.get_device_name(0)}')\n",
                        "    print(f'💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# 📤 Upload dos dados de treinamento\n",
                        "from google.colab import files\n",
                        "import zipfile\n",
                        "import os\n",
                        "\n",
                        "print('📁 Faça upload do arquivo ZIP com os dados de treinamento:')\n",
                        "uploaded = files.upload()\n",
                        "\n",
                        "# Extrair dados\n",
                        "for filename in uploaded.keys():\n",
                        "    if filename.endswith('.zip'):\n",
                        "        with zipfile.ZipFile(filename, 'r') as zip_ref:\n",
                        "            zip_ref.extractall('training_data')\n",
                        "        print(f'✅ Dados extraídos de {filename}')\n",
                        "        break"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        f"# 🧠 Código do modelo Piper TTS\n",
                        self._get_piper_training_code()
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# 🚀 Iniciar treinamento\n",
                        "import piper_train_colab\n",
                        "\n",
                        f"model_name = '{model_name}'\n",
                        "data_dir = 'training_data/data'\n",
                        "\n",
                        "# Configurações de treinamento\n",
                        "config = {\n",
                        "    'language': 'pt-br',\n",
                        "    'sample_rate': 22050,\n",
                        "    'quality': 'high',  # Usar qualidade alta no Colab\n",
                        "    'max_epochs': 200,\n",
                        "    'batch_size': 16,   # GPU permite batch maior\n",
                        "    'use_gpu': True\n",
                        "}\n",
                        "\n",
                        "# Executar treinamento\n",
                        "trainer = piper_train_colab.ColabTrainer(config)\n",
                        "model_path = trainer.train(data_dir, model_name)\n",
                        "\n",
                        "print(f'✅ Treinamento concluído! Modelo salvo em: {model_path}')"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# 📦 Exportar e baixar modelos\n",
                        "import shutil\n",
                        "from google.colab import files\n",
                        "\n",
                        "# Criar pacote final\n",
                        f"output_dir = '{model_name}_trained_model'\n",
                        "os.makedirs(output_dir, exist_ok=True)\n",
                        "\n",
                        "# Copiar arquivos do modelo\n",
                        f"shutil.copy2(f'{model_name}.onnx', f'{output_dir}/{model_name}.onnx')\n",
                        f"shutil.copy2(f'{model_name}.onnx.json', f'{output_dir}/{model_name}.onnx.json')\n",
                        "\n",
                        "# Criar ZIP para download\n",
                        f"zip_filename = '{model_name}_final_model.zip'\n",
                        "shutil.make_archive(zip_filename[:-4], 'zip', output_dir)\n",
                        "\n",
                        "print(f'📥 Baixando modelo treinado: {zip_filename}')\n",
                        "files.download(zip_filename)"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.8.10"
                },
                "accelerator": "GPU"
            },
            "nbformat": 4,
            "nbformat_minor": 0
        }
        
        # Salvar notebook
        notebook_path = scripts_dir / f"{model_name}_colab_training.ipynb"
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=2, ensure_ascii=False)
        
        # Criar código Python para Colab
        self._create_colab_training_code(scripts_dir)
    
    def _create_colab_training_code(self, scripts_dir: Path):
        """Cria código Python otimizado para Colab"""
        
        colab_code = '''#!/usr/bin/env python3
"""
Código de treinamento Piper TTS otimizado para Google Colab
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import pytorch_lightning as pl
from torch.utils.data import Dataset, DataLoader
import librosa
import numpy as np
import json
import csv
import gruut
import soundfile as sf
from pathlib import Path
import os

class ColabPiperDataset(Dataset):
    """Dataset otimizado para Colab"""
    
    def __init__(self, data_dir: str, config: dict):
        self.data_dir = Path(data_dir)
        self.config = config
        self.samples = []
        self.load_metadata()
    
    def load_metadata(self):
        metadata_path = self.data_dir / "metadata.csv"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='|')
            for row in reader:
                if len(row) >= 2:
                    audio_id = row[0]
                    text = row[1] if len(row) == 2 else row[2]
                    audio_path = self.data_dir / "wav" / f"{audio_id}.wav"
                    if audio_path.exists():
                        self.samples.append({
                            'audio_path': str(audio_path),
                            'text': text
                        })
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # Carregar áudio
        audio, sr = librosa.load(sample['audio_path'], sr=self.config['sample_rate'])
        
        # Mel-spectrogram
        mel = librosa.feature.melspectrogram(
            y=audio, sr=sr, n_mels=80, n_fft=1024, 
            hop_length=256, win_length=1024
        )
        mel = librosa.power_to_db(mel, ref=np.max)
        
        # Fonemas
        phonemes = self.text_to_phonemes(sample['text'])
        
        return {
            'mel': torch.FloatTensor(mel),
            'phonemes': torch.LongTensor(phonemes),
            'text': sample['text']
        }
    
    def text_to_phonemes(self, text: str) -> list:
        try:
            phonemes = [1]  # BOS
            for sentence in gruut.sentences(text, lang="pt"):
                for word in sentence:
                    if word.phonemes:
                        for phoneme in word.phonemes:
                            phoneme_id = hash(str(phoneme)) % 254 + 2
                            phonemes.append(phoneme_id)
                    phonemes.append(3)  # Space
            phonemes.append(2)  # EOS
            return phonemes
        except:
            return [1] + [ord(c) % 254 + 2 for c in text[:50]] + [2]

class ColabVITSModel(pl.LightningModule):
    """Modelo VITS otimizado para GPU"""
    
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        
        # Encoder mais robusto
        self.text_encoder = nn.Sequential(
            nn.Embedding(256, 512),
            nn.LSTM(512, 512, num_layers=2, batch_first=True, bidirectional=True),
            nn.Linear(1024, 512),
            nn.Dropout(0.1)
        )
        
        # Decoder com mais camadas
        self.decoder = nn.Sequential(
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Linear(1024, 80)
        )
        
        # Discriminator melhorado
        self.discriminator = nn.Sequential(
            nn.Conv1d(80, 256, 3, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv1d(256, 512, 3, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv1d(512, 256, 3, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv1d(256, 1, 3, padding=1),
            nn.Sigmoid()
        )
    
    def forward(self, phonemes):
        x, _ = self.text_encoder[1](self.text_encoder[0](phonemes))
        x = self.text_encoder[2](x)
        x = self.text_encoder[3](x)
        mel = self.decoder(x)
        return mel.transpose(1, 2)
    
    def training_step(self, batch, batch_idx):
        phonemes = batch['phonemes']
        target_mel = batch['mel']
        
        pred_mel = self(phonemes)
        
        # Ajustar dimensões
        min_len = min(pred_mel.size(-1), target_mel.size(-1))
        pred_mel = pred_mel[:, :, :min_len]
        target_mel = target_mel[:, :, :min_len]
        
        # Losses
        gen_loss = F.mse_loss(pred_mel, target_mel)
        
        real_score = self.discriminator(target_mel)
        fake_score = self.discriminator(pred_mel.detach())
        
        disc_loss = F.binary_cross_entropy(real_score, torch.ones_like(real_score)) + \\
                   F.binary_cross_entropy(fake_score, torch.zeros_like(fake_score))
        
        total_loss = gen_loss + 0.1 * disc_loss
        
        self.log('train_loss', total_loss, prog_bar=True)
        self.log('gen_loss', gen_loss, prog_bar=True)
        self.log('disc_loss', disc_loss, prog_bar=True)
        
        return total_loss
    
    def configure_optimizers(self):
        return torch.optim.AdamW(self.parameters(), lr=2e-4, weight_decay=0.01)

class ColabTrainer:
    """Trainer otimizado para Colab"""
    
    def __init__(self, config: dict):
        self.config = config
    
    def train(self, data_dir: str, model_name: str) -> str:
        print(f"🚀 Iniciando treinamento no Colab para {model_name}")
        
        # Dataset
        dataset = ColabPiperDataset(data_dir, self.config)
        print(f"📊 Dataset: {len(dataset)} amostras")
        
        # DataLoader
        dataloader = DataLoader(
            dataset,
            batch_size=self.config['batch_size'],
            shuffle=True,
            num_workers=2,
            pin_memory=True
        )
        
        # Modelo
        model = ColabVITSModel(self.config)
        
        # Trainer
        trainer = pl.Trainer(
            max_epochs=self.config['max_epochs'],
            accelerator='gpu' if self.config['use_gpu'] else 'cpu',
            devices=1,
            precision=16,  # Mixed precision para GPU
            log_every_n_steps=10,
            enable_checkpointing=True,
            enable_progress_bar=True
        )
        
        # Treinar
        trainer.fit(model, dataloader)
        
        # Exportar
        checkpoint_path = f"{model_name}_final.ckpt"
        trainer.save_checkpoint(checkpoint_path)
        
        # Exportar ONNX
        onnx_path = f"{model_name}.onnx"
        self.export_onnx(model, onnx_path)
        
        # Criar config JSON
        config_path = f"{model_name}.onnx.json"
        self.create_config(config_path, model_name)
        
        return onnx_path
    
    def export_onnx(self, model, output_path: str):
        model.eval()
        dummy_input = torch.randint(0, 256, (1, 50))
        
        torch.onnx.export(
            model, dummy_input, output_path,
            export_params=True, opset_version=11,
            input_names=['phonemes'], output_names=['mel'],
            dynamic_axes={'phonemes': {1: 'seq_len'}, 'mel': {2: 'mel_len'}}
        )
        print(f"✅ Modelo ONNX exportado: {output_path}")
    
    def create_config(self, config_path: str, model_name: str):
        config = {
            "audio": {"sample_rate": self.config['sample_rate']},
            "model": {"type": "vits", "quality": self.config['quality']},
            "inference": {"noise_scale": 0.667, "length_scale": 1.0, "noise_w": 0.8},
            "model_name": model_name,
            "language": self.config['language'],
            "trained_on": "Google Colab GPU"
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Configuração salva: {config_path}")
'''
        
        # Salvar código
        code_path = scripts_dir / "piper_train_colab.py"
        with open(code_path, 'w', encoding='utf-8') as f:
            f.write(colab_code)
    
    def _create_kaggle_notebook(self, model_name: str, scripts_dir: Path, config_dir: Path):
        """Cria notebook do Kaggle"""
        # Similar ao Colab, mas com adaptações para Kaggle
        pass
    
    def _create_codesphere_config(self, model_name: str, scripts_dir: Path, config_dir: Path):
        """Cria configuração do CodeSphere"""
        # Configuração específica para CodeSphere
        pass
    
    def _get_piper_training_code(self) -> str:
        """Retorna código de treinamento inline para notebook"""
        return '''
# Código será inserido aqui automaticamente
import sys
sys.path.append('/content')
        '''
    
    def _create_zip_package(self, source_dir: Path, zip_path: Path):
        """Cria arquivo ZIP do pacote"""
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(source_dir)
                    zipf.write(file_path, arcname)
    
    def get_colab_url(self, notebook_path: str) -> str:
        """Gera URL do Google Colab"""
        # Converter para URL do Colab
        base_url = "https://colab.research.google.com/github/"
        # Implementar lógica de upload para GitHub ou Google Drive
        return f"https://colab.research.google.com/drive/{notebook_path}"

# Estado global para monitoramento
cloud_training_status = {
    'is_exporting': False,
    'platform': '',
    'progress': 0,
    'step': '',
    'package_url': '',
    'notebook_url': ''
}

def get_cloud_status():
    """Retorna status do treinamento em nuvem"""
    return cloud_training_status

def update_cloud_status(step: str, progress: int, **kwargs):
    """Atualiza status do treinamento em nuvem"""
    cloud_training_status.update({
        'step': step,
        'progress': progress,
        **kwargs
    })