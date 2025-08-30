#!/usr/bin/env python3
"""
Script completo de configuração para treinamento de vozes Piper TTS
"""
import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🎤 PIPER TTS - CONFIGURAÇÃO DE TREINAMENTO DE VOZES")
    print("=" * 60)
    print()

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ é necessário. Versão atual:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

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

def install_system_dependencies():
    """Instala dependências do sistema"""
    system = platform.system().lower()
    
    if system == "linux":
        print("\n📦 Instalando dependências do sistema (Linux)...")
        commands = [
            ("sudo apt-get update", "Atualizando lista de pacotes"),
            ("sudo apt-get install -y python3-dev", "Instalando python3-dev"),
            ("sudo apt-get install -y espeak-ng", "Instalando espeak-ng"),
            ("sudo apt-get install -y build-essential", "Instalando build-essential"),
            ("sudo apt-get install -y libsndfile1", "Instalando libsndfile1"),
        ]
        
        for cmd, desc in commands:
            run_command(cmd, desc, check=False)
    
    elif system == "darwin":  # macOS
        print("\n📦 Instalando dependências do sistema (macOS)...")
        commands = [
            ("brew install espeak-ng", "Instalando espeak-ng"),
            ("brew install libsndfile", "Instalando libsndfile"),
        ]
        
        for cmd, desc in commands:
            run_command(cmd, desc, check=False)
    
    elif system == "windows":
        print("\n📦 Sistema Windows detectado")
        print("⚠️  Algumas dependências podem precisar ser instaladas manualmente:")
        print("   - Visual Studio Build Tools")
        print("   - espeak-ng (opcional, para fonemas)")

def create_virtual_environment():
    """Cria ambiente virtual Python"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Ambiente virtual já existe")
        return True
    
    print("\n🐍 Criando ambiente virtual Python...")
    
    # Criar venv
    if not run_command([sys.executable, "-m", "venv", "venv"], 
                      "Criando ambiente virtual"):
        return False
    
    return True

def get_pip_command():
    """Retorna o comando pip correto para o sistema"""
    system = platform.system().lower()
    
    if system == "windows":
        return "venv\\Scripts\\pip.exe"
    else:
        return "venv/bin/pip"

def install_python_dependencies():
    """Instala dependências Python"""
    pip_cmd = get_pip_command()
    
    print(f"\n📚 Instalando dependências Python...")
    
    # Lista de dependências essenciais
    dependencies = [
        "wheel",
        "setuptools",
        "cython>=0.29.0",
        "numpy>=1.19.0",
        "torch>=1.11.0,<2.0.0",
        "pytorch-lightning~=1.7.0",
        "librosa>=0.9.2,<1.0.0",
        "onnxruntime>=1.11.0",
        "piper-phonemize~=1.1.0",
        "soundfile",
        "scipy",
        "tensorboard",
        "matplotlib",
        "flask",
        "flask-cors",
        "werkzeug",
    ]
    
    # Atualizar pip primeiro
    run_command([pip_cmd, "install", "--upgrade", "pip"], 
               "Atualizando pip")
    
    # Instalar dependências uma por uma para melhor controle
    success_count = 0
    for dep in dependencies:
        if run_command([pip_cmd, "install", dep], 
                      f"Instalando {dep}", check=False):
            success_count += 1
    
    print(f"\n📊 Dependências instaladas: {success_count}/{len(dependencies)}")
    return success_count > len(dependencies) * 0.8  # 80% de sucesso

def setup_piper_training():
    """Configura o módulo de treinamento do Piper"""
    print("\n⚙️  Configurando módulo de treinamento Piper...")
    
    # Verificar se o diretório src/python existe
    src_python = Path("src/python")
    if not src_python.exists():
        print("❌ Diretório src/python não encontrado")
        print("   Certifique-se de estar no diretório raiz do projeto Piper")
        return False
    
    pip_cmd = get_pip_command()
    
    # Instalar o módulo piper_train em modo desenvolvimento
    if run_command([pip_cmd, "install", "-e", "src/python"], 
                  "Instalando piper_train"):
        
        # Tentar construir extensão monotonic_align
        build_script = src_python / "build_monotonic_align.sh"
        if build_script.exists() and platform.system().lower() != "windows":
            run_command(["bash", str(build_script)], 
                       "Construindo extensão monotonic_align", check=False)
        
        return True
    
    return False

def create_directory_structure():
    """Cria estrutura de diretórios necessária"""
    print("\n📁 Criando estrutura de diretórios...")
    
    directories = [
        "uploads",
        "training_data", 
        "trained_models",
        "static/audio",
        "templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Criado: {directory}")

def create_example_files():
    """Cria arquivos de exemplo"""
    print("\n📝 Criando arquivos de exemplo...")
    
    # Exemplo de metadata.csv
    metadata_example = """audio001|Olá, este é um exemplo de texto para treinamento de voz.
audio002|A qualidade do áudio é muito importante para bons resultados.
audio003|Recomenda-se pelo menos trinta minutos de áudio limpo e claro.
audio004|O Piper TTS é uma ferramenta poderosa para síntese de voz.
audio005|Com dados suficientes, é possível criar vozes muito naturais."""
    
    example_dir = Path("examples")
    example_dir.mkdir(exist_ok=True)
    
    with open(example_dir / "metadata_example.csv", "w", encoding="utf-8") as f:
        f.write(metadata_example)
    
    # README de instruções
    readme_content = """# Piper TTS - Treinamento de Vozes

## Como usar:

1. **Preparar dados:**
   - Grave arquivos de áudio (.wav) com a voz desejada
   - Crie um arquivo metadata.csv com o formato: id|texto
   - Cada linha deve corresponder a um arquivo de áudio

2. **Iniciar interface:**
   ```bash
   python web_interface.py
   ```

3. **Acessar:** http://localhost:5000

4. **Processo:**
   - Upload dos arquivos na aba "Upload de Dados"
   - Configurar treinamento na aba "Treinamento"
   - Monitorar progresso
   - Testar modelo na aba "Teste de Voz"

## Requisitos de dados:
- Mínimo: 30 minutos de áudio limpo
- Recomendado: 1-2 horas de áudio
- Qualidade: 22kHz, mono, sem ruído de fundo
- Texto: Frases variadas, pontuação correta

## Dicas:
- Use um microfone de boa qualidade
- Grave em ambiente silencioso
- Mantenha tom e velocidade consistentes
- Evite respiração audível entre palavras
"""
    
    with open("INSTRUCOES.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ Arquivos de exemplo criados em 'examples/'")
    print("✅ Instruções criadas em 'INSTRUCOES.md'")

def main():
    print_header()
    
    # Verificações iniciais
    if not check_python_version():
        sys.exit(1)
    
    print("🔍 Verificando sistema...")
    print(f"Sistema operacional: {platform.system()} {platform.release()}")
    print(f"Arquitetura: {platform.machine()}")
    
    # Passos de configuração
    steps = [
        ("Instalando dependências do sistema", install_system_dependencies),
        ("Criando ambiente virtual", create_virtual_environment),
        ("Instalando dependências Python", install_python_dependencies),
        ("Configurando Piper Training", setup_piper_training),
        ("Criando estrutura de diretórios", create_directory_structure),
        ("Criando arquivos de exemplo", create_example_files),
    ]
    
    success_count = 0
    for description, func in steps:
        print(f"\n{'='*50}")
        print(f"📋 {description}")
        print('='*50)
        
        if func():
            success_count += 1
        else:
            print(f"⚠️  Falha em: {description}")
    
    # Resumo final
    print(f"\n{'='*60}")
    print("📊 RESUMO DA CONFIGURAÇÃO")
    print('='*60)
    print(f"✅ Passos concluídos: {success_count}/{len(steps)}")
    
    if success_count == len(steps):
        print("\n🎉 Configuração concluída com sucesso!")
        print("\n📝 Próximos passos:")
        print("1. Ative o ambiente virtual:")
        
        if platform.system().lower() == "windows":
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        
        print("2. Inicie a interface web:")
        print("   python web_interface.py")
        print("3. Acesse: http://localhost:5000")
        print("4. Leia as instruções em INSTRUCOES.md")
        
    else:
        print(f"\n⚠️  Configuração parcial ({success_count}/{len(steps)} passos)")
        print("Verifique os erros acima e tente executar novamente.")
        print("Você pode tentar instalar as dependências faltantes manualmente.")

if __name__ == "__main__":
    main()