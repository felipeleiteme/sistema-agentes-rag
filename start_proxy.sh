#!/bin/bash
# Inicia o LiteLLM Proxy configurado para os modelos locais

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ -d "${ROOT_DIR}/.venv" ]; then
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.venv/bin/activate"
fi

if [ -f "${ROOT_DIR}/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.env"
  set +a
fi

CONFIG_FILE="${ROOT_DIR}/config/litellm_config.yaml"

echo "🚀 Iniciando LiteLLM Proxy na porta 4000..."
echo "📝 Certifique-se de que o Ollama está em execução (brew services start ollama)"

litellm --config "$CONFIG_FILE" --port 4000 "$@"
