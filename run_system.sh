#!/bin/bash
# run_system.sh - Executa o sistema de agentes

cd /Users/Felipe/Documents/Projetos/Agentes/meu_sistema_agentes
source .venv/bin/activate
set -a
source .env
set +a

echo "🤖 Executando sistema de agentes..."
echo "⚠️  Certifique-se que o proxy está rodando em outro terminal!"
echo ""

python3 main.py
