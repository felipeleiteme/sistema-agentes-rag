"""
Módulo de configuração centralizada do projeto.
Carrega variáveis de ambiente e configurações do LiteLLM.
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Classe de configuração centralizada."""

    # Diretórios do projeto
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    CONFIG_DIR = BASE_DIR / "config"
    DATA_DIR = BASE_DIR / "data"
    DOCS_DIR = BASE_DIR / "docs"

    # Chaves API
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    # LiteLLM
    LITELLM_PROXY_URL = os.getenv("LITELLM_PROXY_URL", "http://localhost:4000")
    LITELLM_CONFIG_PATH = CONFIG_DIR / "litellm_config.yaml"

    # Configurações do projeto
    PROJECT_NAME = os.getenv("PROJECT_NAME", "meu_projeto_agentes")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Modelos disponíveis
    MODELS = {
        "gpt4": "gpt-4o",
        "claude_haiku": "claude-haiku",
        "claude_sonnet": "claude-sonnet"
    }

    @classmethod
    def validate(cls) -> bool:
        """Valida se todas as configurações necessárias estão presentes."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY não encontrada no .env")
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY não encontrada no .env")
        if not cls.LITELLM_CONFIG_PATH.exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado: {cls.LITELLM_CONFIG_PATH}")
        return True

    @classmethod
    def get_model_config(cls, model_key: str) -> str:
        """Retorna a configuração do modelo."""
        return cls.MODELS.get(model_key, cls.MODELS["gpt4"])

    @classmethod
    def ensure_directories(cls):
        """Garante que todos os diretórios necessários existam."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.DOCS_DIR.mkdir(exist_ok=True)
        (cls.DATA_DIR / "vectorstore").mkdir(exist_ok=True)


# Validar configurações ao importar
Config.ensure_directories()
