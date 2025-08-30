#!/usr/bin/env python3
"""
Script corrigido para instalar dependências do Piper TTS
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando e mostra o progresso"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        if e.stderr:
            print(f"Saída do erro: {e.stderr}")
        return False

def main():
    print("🚀 Instalando dependências corrigidas do Piper TTS...")
    
    python_cmd = "python" if sys.platform == "win32" else "python3"
    
    # Comandos corrigidos
    commands = [
        # Atualizar pip
        (f"{python_cmd} -m pip install --upgrade pip", "Atualizando pip"),
        
        # Instalar dependências básicas
        (f"{python_cmd} -m pip install --upgrade wheel setuptools", "Instalando wheel e setuptools"),
        (f"{python_cmd} -m pip install cython>=0.29.0", "Instalando Cython"),
        
        # PyTorch primeiro (versão compatível)
        (f"{python_cmd} -m pip install torch>=1.11.0,<2.0.0 torchvision torchaudio", "Instalando PyTorch"),
        
        # PyTorch Lightning versão mais recente compatível
        (f"{python_cmd} -m pip install pytorch-lightning>=1.8.0", "Instalando PyTorch Lightning"),
        
        # Outras dependências de ML
        (f"{python_cmd} -m pip install librosa>=0.9.2", "Instalando librosa"),
        (f"{python_cmd} -m pip install numpy>=1.19.0", "Instalando numpy"),
        (f"{python_cmd} -m pip install onnxruntime>=1.11.0", "Instalando onnxruntime"),
        
        # Dependências de áudio
        (f"{python_cmd} -m pip install soundfile", "Instalando soundfile"),
        (f"{python_cmd} -m pip install scipy", "Instalando scipy"),
        
        # Dependências para interface web
        (f"{python_cmd} -m pip install flask", "Instalando Flask"),
        (f"{python_cmd} -m pip install flask-cors", "Instalando Flask-CORS"),
        (f"{python_cmd} -m pip install werkzeug", "Instalando Werkzeug"),
        
        # Ferramentas de desenvolvimento
        (f"{python_cmd} -m pip install tensorboard", "Instalando TensorBoard"),
        (f"{python_cmd} -m pip install matplotlib", "Instalando matplotlib"),
        
        # Tentar instalar piper-phonemize de forma alternativa
        (f"{python_cmd} -m pip install phonemizer", "Instalando phonemizer (alternativa)"),
    ]
    
    success_count = 0
    total_commands = len(commands)
    
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 Resumo da instalação:")
    print(f"✅ Sucessos: {success_count}/{total_commands}")
    print(f"❌ Falhas: {total_commands - success_count}/{total_commands}")
    
    # Tentar instalar piper-phonemize manualmente se não funcionou
    print(f"\n🔧 Tentando instalar piper-phonemize manualmente...")
    
    # Opções alternativas para piper-phonemize
    alt_commands = [
        f"{python_cmd} -m pip install piper-phonemize==1.1.0",
        f"{python_cmd} -m pip install piper-phonemize>=1.0.0",
        f"{python_cmd} -m pip install git+https://github.com/rhasspy/piper-phonemize.git",
    ]
    
    phonemize_installed = False
    for cmd in alt_commands:
        if run_command(cmd, "Instalando piper-phonemize (alternativa)"):
            phonemize_installed = True
            break
    
    if success_count >= total_commands * 0.8:  # 80% de sucesso
        print("\n🎉 Dependências principais instaladas com sucesso!")
        
        if not phonemize_installed:
            print("\n⚠️  Nota sobre piper-phonemize:")
            print("   - Esta dependência é opcional para a interface web")
            print("   - Você pode usar phonemizer como alternativa")
            print("   - Ou instalar manualmente quando necessário")
        
        print("\n📝 Próximos passos:")
        print("1. Execute 'python web_interface.py' para iniciar a interface")
        print("2. Acesse http://localhost:5000 no navegador")
        print("3. Faça upload dos dados de áudio e texto")
        
    else:
        print(f"\n⚠️  Muitas dependências falharam. Tente:")
        print("1. Atualizar o Python para versão mais recente")
        print("2. Usar um ambiente virtual limpo")
        print("3. Instalar Visual Studio Build Tools (Windows)")

if __name__ == "__main__":
    main()