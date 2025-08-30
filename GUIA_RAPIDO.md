# 🚀 Guia Rápido - Interface Piper TTS

## ✅ Status da Instalação

A interface web foi configurada com sucesso! Você pode começar a usar imediatamente.

### 🎯 Como Acessar
1. Execute: `python web_interface.py`
2. Abra o navegador em: **http://localhost:5000**

## 📋 Passo a Passo Rápido

### 1. Preparar Dados de Áudio
- Grave arquivos de áudio em formato WAV (recomendado)
- Mínimo: 30 minutos de áudio limpo
- Recomendado: 1-2 horas de áudio
- Use microfone de boa qualidade
- Ambiente silencioso, sem eco

### 2. Criar Arquivo Metadata
Use o exemplo em `examples/metadata_exemplo.csv`:
```csv
audio001|Texto correspondente ao áudio 001
audio002|Texto correspondente ao áudio 002
```

### 3. Upload na Interface
- Aba "Upload de Dados"
- Nome do modelo: `minha_voz`
- Selecione arquivos de áudio (.wav)
- Upload do metadata.csv
- Clique "Enviar Arquivos"

### 4. Configurar Treinamento
- Aba "Treinamento"
- Selecione o modelo
- Idioma: Português (Brasil)
- Qualidade: Média
- Clique "Iniciar Treinamento"

### 5. Testar Resultado
- Aba "Teste de Voz"
- Selecione modelo treinado
- Digite texto de teste
- Clique "Gerar Áudio"

## 🔧 Funcionalidades Disponíveis

### ✅ Funcionando:
- Interface web completa
- Upload de arquivos
- Simulação de treinamento
- Gerenciamento de modelos
- Sistema de progresso
- Logs em tempo real

### 🚧 Em Desenvolvimento:
- Integração completa com Piper Train
- Processamento real de áudio
- Geração de modelos ONNX funcionais

## 📁 Estrutura de Arquivos

```
piper/
├── web_interface.py          # Interface principal ✅
├── templates/index.html      # Interface HTML ✅
├── static/
│   ├── css/style.css        # Estilos ✅
│   └── js/script.js         # JavaScript ✅
├── uploads/                 # Arquivos enviados
├── training_data/           # Dados de treinamento
├── trained_models/          # Modelos finalizados
└── examples/                # Arquivos de exemplo ✅
```

## 🎨 Recursos da Interface

### Design Moderno:
- Interface responsiva
- Tema gradiente azul/roxo
- Ícones Font Awesome
- Animações suaves
- Feedback visual em tempo real

### Funcionalidades:
- **Upload:** Drag & drop de arquivos
- **Progresso:** Barra de progresso animada
- **Logs:** Console em tempo real
- **Modelos:** Grid de modelos treinados
- **Teste:** Player de áudio integrado

## 🔍 Próximos Passos

### Para Uso Completo:
1. **Instalar Piper Train:**
   ```bash
   cd src/python
   pip install -e .
   ```

2. **Configurar espeak-ng:**
   - Linux: `sudo apt-get install espeak-ng`
   - Windows: Download manual
   - macOS: `brew install espeak-ng`

3. **Habilitar GPU (opcional):**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### Para Desenvolvimento:
- Modificar `web_interface.py` para integração real
- Adicionar validação de arquivos de áudio
- Implementar conversão de formatos
- Adicionar suporte a múltiplos idiomas

## 🆘 Solução de Problemas

### Interface não carrega:
- Verifique se todas as dependências estão instaladas
- Confirme que a porta 5000 está livre
- Tente acessar http://127.0.0.1:5000

### Upload falha:
- Verifique formato dos arquivos (WAV, MP3, FLAC)
- Confirme que o metadata.csv está correto
- Limite de 500MB por upload

### Treinamento não funciona:
- Atualmente em modo simulação
- Para treinamento real, instale piper_train
- Verifique logs na interface

## 📞 Suporte

- **Documentação:** README_TREINAMENTO.md
- **Exemplos:** Pasta examples/
- **Logs:** Interface web (aba Treinamento)
- **Comunidade:** [Rhasspy Community](https://community.rhasspy.org/)

---

**🎉 Parabéns! Sua interface de treinamento Piper TTS está pronta para uso!**