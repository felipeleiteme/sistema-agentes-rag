"""
Configuração do sistema SAC Learning GEMS
"""
import os
from typing import Optional


class GEMConfig:
    """Configuração do sistema SAC Learning GEMS."""

    # Configurações do LLM - Qwen API (Alibaba Cloud)
    QWEN_API_KEY: str = os.getenv("QWEN_API_KEY", "")
    QWEN_BASE_URL: str = os.getenv("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen-max")  # Modelo Qwen padrão
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))  # Balanceado para criatividade e consistência
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2048"))  # Máximo de tokens na resposta
    LLM_REQUEST_TIMEOUT: float = float(os.getenv("LLM_REQUEST_TIMEOUT", "60.0"))  # Timeout adequado para respostas completas

    @classmethod
    def get_llm_config(cls) -> dict:
        """Retorna a configuração do LLM como dicionário."""
        return {
            "model": cls.LLM_MODEL,
            "temperature": cls.LLM_TEMPERATURE,
            "max_tokens": cls.LLM_MAX_TOKENS,
            "timeout": cls.LLM_REQUEST_TIMEOUT,
            "api_key": cls.QWEN_API_KEY,
            "base_url": cls.QWEN_BASE_URL,
        }