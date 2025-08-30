# 🎤 Como Usar o Sistema de Treinamento Piper TTS

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
