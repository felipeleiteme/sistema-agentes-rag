"""
Configuração do sistema SAC Learning GEMS
"""
import os
from typing import Optional


class GEMConfig:
    """Configuração do sistema SAC Learning GEMS."""
    
    # Configurações do LLM
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.2:3b")  # Modelo disponível
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))  # Balanceado para criatividade e consistência
    LLM_NUM_PREDICT: int = int(os.getenv("LLM_NUM_PREDICT", "2048"))  # Aumentado para evitar respostas cortadas
    LLM_NUM_CTX: int = int(os.getenv("LLM_NUM_CTX", "4096"))         # Aumentado para melhor contexto
    LLM_REQUEST_TIMEOUT: float = float(os.getenv("LLM_REQUEST_TIMEOUT", "60.0"))  # Timeout adequado para respostas completas
    LLM_NUM_THREAD: int = int(os.getenv("LLM_NUM_THREAD", "8"))  # Mais threads para melhor performance
    
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
            "top_k": 40,      # Balanceado para qualidade e velocidade
            "top_p": 0.9,     # Balanceado para qualidade e velocidade
            "repeat_penalty": 1.1,  # Reduz repetições
            "num_gpu": 1,     # Usa GPU se disponível
            "num_batch": 512, # Otimiza processamento em lote
        }