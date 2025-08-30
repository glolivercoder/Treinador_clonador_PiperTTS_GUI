# 🤖 Guia Completo - Automação do CSV

## 🎯 Visão Geral

A **Automação do CSV** elimina a necessidade de criar manualmente o arquivo `metadata.csv`, oferecendo 3 métodos diferentes para gerar automaticamente as transcrições dos seus áudios.

## 🚀 Métodos Disponíveis

### **1. 🎤 Transcrição Automática (IA)**
- **Descrição:** Use inteligência artificial para transcrever automaticamente seus áudios
- **Vantagem:** Totalmente automático, alta precisão
- **Tempo:** 2-10 minutos para 1 hora de áudio
- **Recomendado para:** Qualquer tipo de áudio com fala clara

### **2. 📄 Arquivo de Texto**
- **Descrição:** Faça upload de um arquivo .txt com as transcrições já prontas
- **Vantagem:** Controle total sobre o texto
- **Tempo:** Instantâneo
- **Recomendado para:** Quando você já tem as transcrições

### **3. ✏️ Editor Manual**
- **Descrição:** Edite o CSV diretamente na interface web
- **Vantagem:** Flexibilidade total, correções rápidas
- **Tempo:** Depende da quantidade de texto
- **Recomendado para:** Correções ou datasets pequenos

## 🎤 Transcrição Automática Detalhada

### **Engines Disponíveis:**

#### **🥇 Whisper (OpenAI) - Recomendado**
- **Qualidade:** Excelente (95%+ precisão)
- **Idiomas:** 99+ idiomas suportados
- **Velocidade:** Moderada (2-5x tempo real)
- **Requisitos:** 2GB RAM, funciona offline
- **Melhor para:** Qualquer tipo de áudio

#### **🌐 Google Speech Recognition**
- **Qualidade:** Muito boa (90%+ precisão)
- **Idiomas:** 120+ idiomas
- **Velocidade:** Rápida (tempo real)
- **Requisitos:** Conexão com internet
- **Melhor para:** Áudio limpo, conexão estável

#### **🧠 Wav2Vec2 (Facebook)**
- **Qualidade:** Boa (85%+ precisão)
- **Idiomas:** Principalmente inglês
- **Velocidade:** Rápida (tempo real)
- **Requisitos:** 4GB RAM, funciona offline
- **Melhor para:** Áudio em inglês

### **Processo de Transcrição:**

#### **Passo 1: Preparação**
```bash
# Instalar dependências
python install_transcription_deps.py
```

#### **Passo 2: Configuração**
1. **Selecione o modelo** que contém os áudios
2. **Escolha o engine** (Whisper recomendado)
3. **Defina o idioma** dos áudios
4. **Marque "Revisar"** se quiser verificar antes de salvar

#### **Passo 3: Execução**
1. Clique **"Iniciar Transcrição Automática"**
2. **Acompanhe o progresso** em tempo real
3. **Revise os resultados** na lista
4. **CSV é gerado** automaticamente

#### **Passo 4: Verificação**
- ✅ **Arquivos processados:** Quantos foram transcritos
- ✅ **Taxa de sucesso:** Percentual de sucessos
- ✅ **Erros encontrados:** Lista de problemas
- ✅ **Tempo total:** Duração do processo

### **Configurações Avançadas:**

#### **Otimização por Tipo de Áudio:**

**📻 Podcast/Narração:**
- Engine: Whisper
- Configuração: Padrão
- Pós-processamento: Ativado

**🎵 Música com Vocal:**
- Engine: Whisper
- Configuração: Modelo large
- Filtro de ruído: Ativado

**📞 Chamadas/Baixa Qualidade:**
- Engine: Google
- Pré-processamento: Normalização
- Tolerância a erros: Alta

**🎭 Múltiplos Falantes:**
- Engine: Whisper
- Detecção de falantes: Ativada
- Formato: id|falante|texto

## 📄 Arquivo de Texto Detalhado

### **Formato do Arquivo:**
```
Primeira linha de texto para audio001.wav
Segunda linha de texto para audio002.wav
Terceira linha de texto para audio003.wav
...
```

### **Regras Importantes:**
1. **Uma linha por áudio** na ordem alfabética dos arquivos
2. **Codificação UTF-8** para acentos e caracteres especiais
3. **Sem linhas vazias** no meio do arquivo
4. **Texto limpo** sem formatação especial

### **Exemplo Prático:**
```
Olá, bem-vindos ao nosso podcast sobre tecnologia.
Hoje vamos falar sobre inteligência artificial e suas aplicações.
A IA está revolucionando diversos setores da economia.
Vamos começar com os conceitos básicos de machine learning.
```

### **Ferramentas Recomendadas:**
- **Notepad++** (Windows) - Controle de codificação
- **VS Code** (Multiplataforma) - Editor avançado
- **Sublime Text** (Multiplataforma) - Leve e rápido
- **Nano/Vim** (Linux) - Editores de terminal

## ✏️ Editor Manual Detalhado

### **Interface do Editor:**
- **Área de texto** com syntax highlighting
- **Validação em tempo real** do formato
- **Numeração de linhas** para facilitar edição
- **Botões de ação** (Carregar, Validar, Salvar)

### **Formato Suportado:**

#### **Falante Único:**
```
audio001|Texto correspondente ao primeiro áudio
audio002|Texto correspondente ao segundo áudio
audio003|Texto correspondente ao terceiro áudio
```

#### **Múltiplos Falantes:**
```
audio001|João|Olá, meu nome é João
audio002|Maria|Oi, eu sou a Maria
audio003|João|Vamos começar nossa conversa
```

### **Funcionalidades do Editor:**

#### **🔍 Validação Automática:**
- ✅ **Formato correto** (separadores |)
- ✅ **IDs únicos** sem duplicatas
- ✅ **Texto não vazio** em todas as linhas
- ⚠️ **Avisos** para possíveis problemas
- ❌ **Erros** que impedem o salvamento

#### **📁 Carregar Existente:**
- Carrega CSV já criado para edição
- Preserva formatação original
- Permite correções pontuais

#### **💾 Salvamento Inteligente:**
- Backup automático antes de salvar
- Validação final antes de confirmar
- Mensagem de sucesso/erro

### **Dicas de Edição:**

#### **Atalhos Úteis:**
- **Ctrl+A:** Selecionar tudo
- **Ctrl+F:** Buscar e substituir
- **Ctrl+Z:** Desfazer
- **Ctrl+Y:** Refazer

#### **Correções Comuns:**
```bash
# Substituir vírgulas por pipes
Buscar: ,
Substituir: |

# Remover espaços extras
Buscar: \s+
Substituir: (espaço único)

# Padronizar IDs
Buscar: audio(\d+)
Substituir: audio00$1
```

## 🔧 Solução de Problemas

### **Problemas de Transcrição:**

#### **❌ "Engine não disponível"**
**Solução:**
```bash
# Instalar dependências
python install_transcription_deps.py

# Verificar instalação
python -c "import whisper; print('Whisper OK')"
```

#### **❌ "Erro de memória"**
**Solução:**
- Use engine Google (menos RAM)
- Processe em lotes menores
- Feche outros programas

#### **❌ "Transcrição imprecisa"**
**Solução:**
- Melhore qualidade do áudio
- Use Whisper com modelo large
- Revise e corrija manualmente

### **Problemas de Arquivo de Texto:**

#### **❌ "Número de linhas não confere"**
**Solução:**
- Conte arquivos de áudio: `ls wav/*.wav | wc -l`
- Conte linhas do texto: `wc -l texto.txt`
- Ajuste o arquivo para ter o mesmo número

#### **❌ "Caracteres especiais quebrados"**
**Solução:**
- Salve em UTF-8
- Use editor que suporte Unicode
- Teste com caracteres: áéíóú ção

### **Problemas do Editor:**

#### **❌ "Validação falha"**
**Solução:**
- Verifique separadores |
- Remova linhas vazias
- Confirme IDs únicos

#### **❌ "Não consegue salvar"**
**Solução:**
- Corrija erros de validação
- Verifique permissões de arquivo
- Tente editor manual como backup

## 📊 Comparação de Métodos

| Método | Velocidade | Precisão | Controle | Dificuldade |
|--------|------------|----------|----------|-------------|
| **Transcrição IA** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐ |
| **Arquivo Texto** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Editor Manual** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🎯 Recomendações por Cenário

### **🆕 Primeiro Uso:**
1. **Transcrição Automática** com Whisper
2. **Revisar resultados** no editor
3. **Fazer correções** se necessário

### **📚 Dataset Grande (100+ áudios):**
1. **Transcrição Automática** em lotes
2. **Validação automática** de qualidade
3. **Correção manual** apenas dos erros

### **🎯 Máxima Precisão:**
1. **Arquivo de Texto** com transcrições manuais
2. **Validação** no editor
3. **Teste** com alguns áudios primeiro

### **🔄 Correções Rápidas:**
1. **Editor Manual** para mudanças pontuais
2. **Carregar CSV existente**
3. **Salvar** após correções

## 🚀 Fluxo Recomendado Completo

### **Etapa 1: Preparação (5 min)**
```bash
# 1. Instalar dependências
python install_transcription_deps.py

# 2. Organizar arquivos
mkdir meu_modelo/wav
# Copiar arquivos .wav para a pasta
```

### **Etapa 2: Upload (2 min)**
1. Acesse aba "Upload de Dados"
2. Digite nome do modelo
3. Selecione arquivos de áudio
4. **NÃO** envie metadata.csv ainda

### **Etapa 3: Automação (10-30 min)**
1. Clique "Automação do CSV"
2. Escolha "Transcrição Automática"
3. Configure: Whisper + Português
4. Inicie transcrição
5. Aguarde conclusão

### **Etapa 4: Validação (5 min)**
1. Revise resultados na interface
2. Corrija erros no editor se necessário
3. Valide formato final

### **Etapa 5: Treinamento**
1. Vá para aba "Treinamento"
2. Configure parâmetros
3. Inicie treinamento do modelo

---

**🎉 Com a Automação do CSV, você economiza horas de trabalho manual e garante transcrições precisas para treinar modelos de voz de alta qualidade!**