#!/usr/bin/env python3
"""
Script para instalar dependências de transcrição automática
"""
import subprocess
import sys
import platform

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
            print(f"Detalhes: {e.stderr}")
        return False

def main():
    print("🎤 Instalando dependências para transcrição automática...")
    
    python_cmd = "python" if sys.platform == "win32" else "python3"
    
    # Lista de dependências para transcrição
    dependencies = [
        # Whisper (OpenAI) - Recomendado
        ("openai-whisper", "Whisper (OpenAI) - Transcrição de alta qualidade"),
        
        # SpeechRecognition - Google/Offline
        ("SpeechRecognition", "SpeechRecognition - Múltiplos engines"),
        ("pyaudio", "PyAudio - Suporte a microfone (opcional)"),
        
        # Transformers - Wav2Vec2 e outros modelos
        ("transformers[torch]", "Transformers - Modelos Hugging Face"),
        
        # Processamento de áudio
        ("librosa>=0.9.2", "Librosa - Processamento de áudio"),
        ("soundfile", "SoundFile - Leitura/escrita de áudio"),
        ("scipy", "SciPy - Processamento científico"),
        
        # Dependências opcionais
        ("torch", "PyTorch - Framework de ML"),
        ("torchaudio", "TorchAudio - Áudio para PyTorch"),
    ]
    
    success_count = 0
    total_deps = len(dependencies)
    
    print(f"📦 Instalando {total_deps} dependências...")
    
    for package, description in dependencies:
        if run_command(f"{python_cmd} -m pip install {package}", description):
            success_count += 1
    
    # Dependências específicas do sistema
    system = platform.system().lower()
    
    if system == "linux":
        print("\n🐧 Instalando dependências do sistema Linux...")
        system_deps = [
            ("sudo apt-get update", "Atualizando lista de pacotes"),
            ("sudo apt-get install -y ffmpeg", "Instalando FFmpeg"),
            ("sudo apt-get install -y portaudio19-dev", "Instalando PortAudio"),
        ]
        
        for cmd, desc in system_deps:
            run_command(cmd, desc)
    
    elif system == "darwin":  # macOS
        print("\n🍎 Instalando dependências do macOS...")
        system_deps = [
            ("brew install ffmpeg", "Instalando FFmpeg"),
            ("brew install portaudio", "Instalando PortAudio"),
        ]
        
        for cmd, desc in system_deps:
            run_command(cmd, desc)
    
    elif system == "windows":
        print("\n🪟 Sistema Windows detectado")
        print("💡 FFmpeg pode ser necessário para alguns formatos de áudio")
        print("   Baixe em: https://ffmpeg.org/download.html")
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DA INSTALAÇÃO")
    print('='*60)
    print(f"✅ Dependências instaladas: {success_count}/{total_deps}")
    
    if success_count >= total_deps * 0.8:  # 80% de sucesso
        print("\n🎉 Instalação concluída com sucesso!")
        
        print("\n🎯 Engines de transcrição disponíveis:")
        print("✅ Whisper (OpenAI) - Recomendado para qualidade")
        print("✅ Google Speech Recognition - Requer internet")
        print("✅ Wav2Vec2 (Facebook) - Modelo local")
        
        print("\n📝 Como usar:")
        print("1. Faça upload dos arquivos de áudio")
        print("2. Vá para aba 'Upload de Dados'")
        print("3. Clique em 'Automação do CSV'")
        print("4. Escolha 'Transcrição Automática'")
        print("5. Selecione o engine e idioma")
        print("6. Clique 'Iniciar Transcrição Automática'")
        
        print("\n⚡ Dicas de performance:")
        print("• Whisper: Melhor qualidade, mais lento")
        print("• Google: Rápido, requer internet")
        print("• Wav2Vec2: Local, boa para inglês")
        
    else:
        print(f"\n⚠️  Instalação parcial ({success_count}/{total_deps})")
        print("Algumas funcionalidades podem não estar disponíveis.")
        print("Tente instalar manualmente as dependências que falharam.")
    
    # Teste rápido
    print(f"\n🧪 Testando instalação...")
    
    try:
        import whisper
        print("✅ Whisper - OK")
    except ImportError:
        print("❌ Whisper - Não disponível")
    
    try:
        import speech_recognition
        print("✅ SpeechRecognition - OK")
    except ImportError:
        print("❌ SpeechRecognition - Não disponível")
    
    try:
        from transformers import pipeline
        print("✅ Transformers - OK")
    except ImportError:
        print("❌ Transformers - Não disponível")
    
    try:
        import librosa
        print("✅ Librosa - OK")
    except ImportError:
        print("❌ Librosa - Não disponível")

if __name__ == "__main__":
    main()