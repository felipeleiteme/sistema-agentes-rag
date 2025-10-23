#!/bin/bash
# start_proxy.sh - Inicia o LiteLLM Proxy

cd /Users/Felipe/Documents/Projetos/Agentes/meu_sistema_agentes
source .venv/bin/activate
set -a
source .env
set +a

echo "🚀 Iniciando LiteLLM Proxy na porta 4000..."
echo "📝 Certifique-se que o Ollama está rodando: brew services start ollama"
echo ""

litellm --config config.yaml --port 4000
