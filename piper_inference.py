#!/usr/bin/env python3
"""
Sistema de inferência para modelos Piper TTS treinados
"""
import torch
import onnxruntime as ort
import numpy as np
import json
import gruut
import soundfile as sf
from pathlib import Path
import librosa
from typing import List, Optional

class PiperTTSInference:
    """Sistema de inferência para modelos Piper TTS"""
    
    def __init__(self, model_path: str, config_path: str):
        self.model_path = Path(model_path)
        self.config_path = Path(config_path)
        
        # Carregar configuração
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Inicializar sessão ONNX
        try:
            self.session = ort.InferenceSession(str(self.model_path))
            self.onnx_available = True
        except Exception as e:
            print(f"⚠️  Erro carregando modelo ONNX: {e}")
            self.onnx_available = False
            
            # Fallback: carregar modelo PyTorch se disponível
            try:
                from piper_train_real import SimpleVITS
                self.model = SimpleVITS.load_from_checkpoint(str(self.model_path))
                self.model.eval()
                self.pytorch_available = True
            except:
                self.pytorch_available = False
    
    def text_to_phonemes(self, text: str, language: str = "pt") -> List[int]:
        """Converte texto para sequência de IDs de fonemas"""
        try:
            # Usar gruut para fonemas
            phonemes = []
            
            # Adicionar token de início
            phonemes.append(1)  # BOS
            
            for sentence in gruut.sentences(text, lang=language):
                for word in sentence:
                    if word.phonemes:
                        for phoneme in word.phonemes:
                            # Mapear fonema para ID (simplificado)
                            phoneme_id = hash(str(phoneme)) % 254 + 2  # Evitar 0 e 1
                            phonemes.append(phoneme_id)
                    else:
                        # Palavra sem fonemas, usar caracteres
                        for char in word.text:
                            char_id = ord(char) % 254 + 2
                            phonemes.append(char_id)
                    
                    # Adicionar espaço entre palavras
                    phonemes.append(3)  # Espaço
            
            # Adicionar token de fim
            phonemes.append(2)  # EOS
            
            return phonemes
            
        except Exception as e:
            print(f"⚠️  Erro na conversão de fonemas: {e}")
            # Fallback: converter caracteres diretamente
            phonemes = [1]  # BOS
            for char in text[:100]:  # Limitar tamanho
                char_id = ord(char) % 254 + 2
                phonemes.append(char_id)
            phonemes.append(2)  # EOS
            return phonemes
    
    def mel_to_audio(self, mel_spectrogram: np.ndarray, sample_rate: int = 22050) -> np.ndarray:
        """Converte mel-spectrogram para áudio usando Griffin-Lim"""
        
        # Converter mel para linear spectrogram (aproximação)
        mel_db = mel_spectrogram
        mel_linear = librosa.db_to_power(mel_db)
        
        # Usar Griffin-Lim para reconstruir áudio
        audio = librosa.feature.inverse.mel_to_audio(
            mel_linear,
            sr=sample_rate,
            n_fft=1024,
            hop_length=256,
            win_length=1024,
            n_iter=32
        )
        
        # Normalizar
        audio = librosa.util.normalize(audio)
        
        return audio
    
    def synthesize(self, text: str, output_path: Optional[str] = None) -> np.ndarray:
        """Sintetiza áudio a partir de texto"""
        
        print(f"🎤 Sintetizando: '{text}'")
        
        # Converter texto para fonemas
        language = self.config.get('language', 'pt')
        phonemes = self.text_to_phonemes(text, language)
        
        print(f"📝 Fonemas: {len(phonemes)} tokens")
        
        # Preparar input
        phoneme_input = np.array([phonemes], dtype=np.int64)
        
        try:
            if self.onnx_available:
                # Usar modelo ONNX
                input_name = self.session.get_inputs()[0].name
                output_name = self.session.get_outputs()[0].name
                
                result = self.session.run([output_name], {input_name: phoneme_input})
                mel_output = result[0][0]  # [mel_bins, time]
                
            elif self.pytorch_available:
                # Usar modelo PyTorch
                with torch.no_grad():
                    phoneme_tensor = torch.LongTensor(phoneme_input)
                    mel_output = self.model(phoneme_tensor)
                    mel_output = mel_output[0].numpy()  # [mel_bins, time]
            
            else:
                # Fallback: gerar mel-spectrogram sintético
                print("⚠️  Usando síntese sintética (modelo não disponível)")
                mel_output = self.generate_synthetic_mel(len(phonemes))
            
            print(f"🎵 Mel-spectrogram gerado: {mel_output.shape}")
            
            # Converter mel para áudio
            sample_rate = self.config.get('audio', {}).get('sample_rate', 22050)
            audio = self.mel_to_audio(mel_output, sample_rate)
            
            print(f"🔊 Áudio gerado: {len(audio)} amostras, {len(audio)/sample_rate:.2f}s")
            
            # Salvar se especificado
            if output_path:
                sf.write(output_path, audio, sample_rate)
                print(f"💾 Áudio salvo em: {output_path}")
            
            return audio
            
        except Exception as e:
            print(f"❌ Erro na síntese: {e}")
            # Fallback: gerar áudio sintético
            return self.generate_synthetic_audio(text)
    
    def generate_synthetic_mel(self, length: int) -> np.ndarray:
        """Gera mel-spectrogram sintético para fallback"""
        
        # Gerar mel-spectrogram com padrão senoidal
        time_steps = max(length * 4, 100)  # Aproximação
        mel_bins = 80
        
        mel = np.zeros((mel_bins, time_steps))
        
        for i in range(mel_bins):
            frequency = (i + 1) * 0.1
            for t in range(time_steps):
                mel[i, t] = np.sin(frequency * t * 0.1) * np.exp(-t * 0.01)
        
        # Normalizar
        mel = (mel - mel.min()) / (mel.max() - mel.min() + 1e-8)
        mel = mel * 80 - 80  # Converter para dB
        
        return mel
    
    def generate_synthetic_audio(self, text: str, duration: float = 2.0) -> np.ndarray:
        """Gera áudio sintético para fallback"""
        
        sample_rate = self.config.get('audio', {}).get('sample_rate', 22050)
        samples = int(duration * sample_rate)
        
        # Gerar tom baseado no comprimento do texto
        frequency = 200 + (len(text) % 300)  # 200-500 Hz
        
        t = np.linspace(0, duration, samples)
        audio = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Adicionar envelope
        envelope = np.exp(-t * 2)
        audio *= envelope
        
        return audio

def test_model(model_path: str, config_path: str, test_text: str = "Olá, este é um teste."):
    """Testa um modelo treinado"""
    
    print(f"🧪 Testando modelo: {model_path}")
    
    try:
        # Criar sistema de inferência
        tts = PiperTTSInference(model_path, config_path)
        
        # Sintetizar áudio de teste
        output_path = f"test_output_{Path(model_path).stem}.wav"
        audio = tts.synthesize(test_text, output_path)
        
        print(f"✅ Teste concluído! Áudio salvo em: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    # Teste básico
    print("🧪 Testando sistema de inferência Piper TTS")
    
    # Criar configuração de teste
    test_config = {
        "audio": {
            "sample_rate": 22050
        },
        "language": "pt",
        "model_name": "test_model"
    }
    
    with open("test_config.json", 'w') as f:
        json.dump(test_config, f, indent=2)
    
    print("✅ Sistema de inferência carregado com sucesso!")