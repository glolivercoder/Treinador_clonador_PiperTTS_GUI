#!/usr/bin/env python3
"""
Script para instalar todas as dependências necessárias para o treinamento do Piper TTS
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        print(f"Saída do erro: {e.stderr}")
        return False

def main():
    print("🚀 Instalando dependências do Piper TTS para treinamento de vozes...")
    
    # Verificar se Python está disponível
    python_cmd = "python" if sys.platform == "win32" else "python3"
    
    # Lista de comandos para instalar dependências
    commands = [
        # Atualizar pip
        (f"{python_cmd} -m pip install --upgrade pip", "Atualizando pip"),
        
        # Instalar wheel e setuptools
        (f"{python_cmd} -m pip install --upgrade wheel setuptools", "Instalando wheel e setuptools"),
        
        # Instalar dependências principais do Piper
        (f"{python_cmd} -m pip install cython>=0.29.0", "Instalando Cython"),
        (f"{python_cmd} -m pip install piper-phonemize~=1.1.0", "Instalando piper-phonemize"),
        (f"{python_cmd} -m pip install librosa>=0.9.2", "Instalando librosa"),
        (f"{python_cmd} -m pip install numpy>=1.19.0", "Instalando numpy"),
        (f"{python_cmd} -m pip install onnxruntime>=1.11.0", "Instalando onnxruntime"),
        (f"{python_cmd} -m pip install pytorch-lightning~=1.7.0", "Instalando pytorch-lightning"),
        (f"{python_cmd} -m pip install torch>=1.11.0", "Instalando PyTorch"),
        
        # Dependências para interface web
        (f"{python_cmd} -m pip install flask", "Instalando Flask"),
        (f"{python_cmd} -m pip install flask-cors", "Instalando Flask-CORS"),
        (f"{python_cmd} -m pip install werkzeug", "Instalando Werkzeug"),
        
        # Dependências para processamento de áudio
        (f"{python_cmd} -m pip install soundfile", "Instalando soundfile"),
        (f"{python_cmd} -m pip install scipy", "Instalando scipy"),
        
        # Dependências para desenvolvimento
        (f"{python_cmd} -m pip install tensorboard", "Instalando TensorBoard"),
        (f"{python_cmd} -m pip install matplotlib", "Instalando matplotlib"),
    ]
    
    success_count = 0
    total_commands = len(commands)
    
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 Resumo da instalação:")
    print(f"✅ Sucessos: {success_count}/{total_commands}")
    print(f"❌ Falhas: {total_commands - success_count}/{total_commands}")
    
    if success_count == total_commands:
        print("\n🎉 Todas as dependências foram instaladas com sucesso!")
        print("\n📝 Próximos passos:")
        print("1. Execute 'python web_interface.py' para iniciar a interface web")
        print("2. Acesse http://localhost:5000 no seu navegador")
        print("3. Faça upload dos seus dados de áudio e texto para começar o treinamento")
    else:
        print(f"\n⚠️  Algumas dependências falharam. Verifique os erros acima.")
        print("Você pode tentar instalar manualmente as dependências que falharam.")

if __name__ == "__main__":
    main()