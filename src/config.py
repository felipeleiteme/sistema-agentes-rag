"""
Configuração do sistema SAC Learning GEMS
"""
import os
from typing import Optional


class GEMConfig:
    """Configuração do sistema SAC Learning GEMS."""
    
    # Configurações do LLM
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2:1b")  # Modelo mais rápido por padrão
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.6"))  # Aumentado para respostas mais rápidas
    LLM_NUM_PREDICT: int = int(os.getenv("LLM_NUM_PREDICT", "150"))  # Reduzido para respostas mais rápidas
    LLM_NUM_CTX: int = int(os.getenv("LLM_NUM_CTX", "1024"))         # Reduzido para processamento mais rápido
    LLM_REQUEST_TIMEOUT: float = float(os.getenv("LLM_REQUEST_TIMEOUT", "15.0"))  # Timeout mais curto
    LLM_NUM_THREAD: int = int(os.getenv("LLM_NUM_THREAD", "4"))
    
    @classmethod
    def get_llm_config(cls) -> dict:
        """Retorna a configuração do LLM como dicionário."""
        return {
            "model": cls.LLM_MODEL,
            "temperature": cls.LLM_TEMPERATURE,
            "num_predict": cls.LLM_NUM_PREDICT,
            "num_ctx": cls.LLM_NUM_CTX,
            "request_timeout": cls.LLM_REQUEST_TIMEOUT,
            "num_thread": cls.LLM_NUM_THREAD,
        }