#!/usr/bin/env python3
"""
Configuração completa do ambiente Piper TTS para treinamento real de vozes
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    print("=" * 70)
    print("🎤 PIPER TTS - CONFIGURAÇÃO COMPLETA PARA TREINAMENTO REAL")
    print("=" * 70)
    print()

def run_command(command, description, check=True):
    """Executa um comando e mostra o progresso"""
    print(f"\n🔄 {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, 
                                  capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} - Concluído")
            return True
        else:
            print(f"⚠️  {description} - Aviso: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        if e.stderr:
            print(f"Detalhes: {e.stderr}")
        return False

def install_dependencies():
    """Instala todas as dependências necessárias"""
    print("\n📦 Instalando dependências Python...")
    
    python_cmd = "python" if sys.platform == "win32" else "python3"
    
    # Dependências essenciais
    dependencies = [
        "torch>=1.11.0",
        "torchvision", 
        "torchaudio",
        "pytorch-lightning>=1.8.0",
        "librosa>=0.9.2",
        "numpy>=1.19.0",
        "scipy",
        "soundfile",
        "onnxruntime>=1.11.0",
        "gruut>=2.0.0",
        "phonemizer",
        "flask",
        "flask-cors",
        "werkzeug",
        "tensorboard",
        "matplotlib",
        "cython>=0.29.0"
    ]
    
    success_count = 0
    
    # Atualizar pip primeiro
    run_command([python_cmd, "-m", "pip", "install", "--upgrade", "pip"], 
               "Atualizando pip")
    
    # Instalar PyTorch com CPU
    if run_command([python_cmd, "-m", "pip", "install", "torch", "torchvision", 
                   "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"], 
                  "Instalando PyTorch (CPU)"):
        success_count += 1
    
    # Instalar outras dependências
    for dep in dependencies[3:]:  # Pular torch, torchvision, torchaudio
        if run_command([python_cmd, "-m", "pip", "install", dep], 
                      f"Instalando {dep}", check=False):
            success_count += 1
    
    print(f"\n📊 Dependências instaladas: {success_count}/{len(dependencies)}")
    return success_count > len(dependencies) * 0.8

def create_directory_structure():
    """Cria estrutura de diretórios"""
    print("\n📁 Criando estrutura de diretórios...")
    
    directories = [
        "uploads",
        "training_data",
        "trained_models", 
        "static/audio",
        "static/css",
        "static/js",
        "templates",
        "examples",
        "checkpoints",
        "logs"
    ]
    
    try:
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ Criado: {directory}")
        return True
    except Exception as e:
        print(f"❌ Erro criando diretórios: {e}")
        return False

def create_example_data():
    """Cria dados de exemplo para teste"""
    print("\n📝 Criando dados de exemplo...")
    
    try:
        # Metadata de exemplo
        metadata_content = """audio001|Olá, este é um exemplo de texto para treinamento de voz clonada.
audio002|A qualidade do áudio é muito importante para obter bons resultados.
audio003|Recomenda-se pelo menos trinta minutos de áudio limpo e claro.
audio004|O Piper TTS é uma ferramenta poderosa para síntese de voz neural.
audio005|Com dados suficientes, é possível criar vozes muito naturais.
audio006|A consistência na gravação é fundamental para o sucesso do modelo.
audio007|Use um microfone de boa qualidade em ambiente silencioso.
audio008|Evite respiração audível e ruídos de fundo durante a gravação.
audio009|Textos variados ajudam o modelo a aprender melhor a pronúncia.
audio010|O treinamento pode levar algumas horas dependendo da quantidade de dados."""
        
        examples_dir = Path("examples")
        with open(examples_dir / "metadata_exemplo.csv", "w", encoding="utf-8") as f:
            f.write(metadata_content)
        
        # Instruções de uso
        instructions = """# 🎤 Como Usar o Sistema de Treinamento Piper TTS

## 1. Preparar Dados de Áudio
- Grave arquivos de áudio em formato WAV (22kHz, mono)
- Mínimo: 30 minutos de áudio limpo
- Recomendado: 1-2 horas de áudio de qualidade

## 2. Criar Metadata
- Use o formato: audio_id|texto_correspondente
- Exemplo disponível em: examples/metadata_exemplo.csv

## 3. Iniciar Interface
```bash
python web_interface.py
```

## 4. Acessar Interface
- Abra: http://localhost:5000
- Siga o fluxo: Upload → Treinamento → Teste

## 5. Monitorar Progresso
- Acompanhe logs em tempo real
- Verifique métricas de loss
- Aguarde conclusão do treinamento

## 6. Testar Modelo
- Use a aba "Teste de Voz"
- Digite texto personalizado
- Ouça resultado sintetizado
"""
        
        with open("COMO_USAR.md", "w", encoding="utf-8") as f:
            f.write(instructions)
        
        print("✅ Dados de exemplo criados")
        return True
        
    except Exception as e:
        print(f"❌ Erro criando dados de exemplo: {e}")
        return False

def test_installation():
    """Testa se a instalação está funcionando"""
    print("\n🧪 Testando instalação...")
    
    try:
        # Testar imports principais
        import torch
        import pytorch_lightning as pl
        import librosa
        import gruut
        import flask
        import onnxruntime
        
        print("✅ Todos os módulos importados com sucesso")
        
        # Testar módulos customizados
        import piper_train_real
        import piper_inference
        
        print("✅ Módulos customizados carregados")
        
        # Testar PyTorch
        tensor = torch.randn(2, 3)
        print(f"✅ PyTorch funcionando: {tensor.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    print_header()
    
    print("🔍 Verificando sistema...")
    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Arquitetura: {platform.machine()}")
    
    # Lista de passos
    steps = [
        ("Instalando dependências", install_dependencies),
        ("Criando estrutura de diretórios", create_directory_structure),
        ("Criando dados de exemplo", create_example_data),
        ("Testando instalação", test_installation),
    ]
    
    success_count = 0
    
    for description, func in steps:
        print(f"\n{'='*60}")
        print(f"📋 {description}")
        print('='*60)
        
        if func():
            success_count += 1
        else:
            print(f"⚠️  Falha em: {description}")
    
    # Resumo final
    print(f"\n{'='*70}")
    print("📊 RESUMO DA CONFIGURAÇÃO")
    print('='*70)
    print(f"✅ Passos concluídos: {success_count}/{len(steps)}")
    
    if success_count == len(steps):
        print("\n🎉 CONFIGURAÇÃO COMPLETA COM SUCESSO!")
        print("\n🚀 Sistema Piper TTS pronto para treinamento real de vozes!")
        print("\n📝 Próximos passos:")
        print("1. Prepare seus dados de áudio (WAV, 22kHz)")
        print("2. Crie arquivo metadata.csv (veja examples/)")
        print("3. Execute: python web_interface.py")
        print("4. Acesse: http://localhost:5000")
        print("5. Siga o fluxo: Upload → Treinamento → Teste")
        
        print("\n🎯 Recursos disponíveis:")
        print("✅ Treinamento real com PyTorch Lightning")
        print("✅ Pré-processamento automático de áudio")
        print("✅ Conversão texto-fonema com Gruut")
        print("✅ Exportação para ONNX")
        print("✅ Sistema de inferência integrado")
        print("✅ Interface web moderna e responsiva")
        print("✅ Monitoramento em tempo real")
        
        print("\n📚 Documentação:")
        print("- COMO_USAR.md - Instruções detalhadas")
        print("- examples/ - Dados de exemplo")
        print("- README_TREINAMENTO.md - Guia completo")
        
    else:
        print(f"\n⚠️  Configuração parcial ({success_count}/{len(steps)} passos)")
        print("Alguns componentes podem não funcionar corretamente.")
        print("Verifique os erros acima e tente novamente.")

if __name__ == "__main__":
    main()