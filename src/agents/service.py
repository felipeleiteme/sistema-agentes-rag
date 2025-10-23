"""Serviço de roteamento de perguntas para os agentes (LEGADO - Não usado mais)."""

from dataclasses import dataclass
from typing import Iterable, Optional

from langchain_ollama import ChatOllama


@dataclass
class AgentResponse:
    """Representa a resposta produzida por um agente."""

    answer: str
    agent: str
    used_context: bool
    context_preview: Optional[str] = None
    error: Optional[str] = None


class AgentService:
    """Encapsula a lógica de decisão e resposta dos agentes."""

    def __init__(
        self,
        llm: Optional[ChatOllama] = None,
        knowledge_tool=None,
        hr_keywords: Optional[Iterable[str]] = None,
    ) -> None:
        self.llm = llm or ChatOllama(
            model="llama3.2:3b",
            temperature=0.5,
            num_predict=150,
            request_timeout=20.0,
        )
        self.knowledge_tool = knowledge_tool
        self.hr_keywords = tuple(
            hr_keywords
            or (
                "férias",
                "ferias",
                "salário",
                "salario",
                "bônus",
                "bonus",
                "contrato",
                "clt",
                "pj",
                "folga",
                "licença",
                "licenca",
                "benefícios",
                "beneficios",
                "rh",
                "funcionário",
                "funcionario",
            )
        )

    def classify_question(self, question: str) -> str:
        """Classifica a pergunta entre o agente de RH e o assistente geral."""

        lowered = question.lower()
        return "hr" if any(keyword in lowered for keyword in self.hr_keywords) else "general"

    def answer_question(self, question: str) -> AgentResponse:
        """Retorna a resposta do agente apropriado para a pergunta informada."""

        try:
            agent_key = self.classify_question(question)
            if agent_key == "hr":
                return self._handle_hr_question(question)
            return self._handle_general_question(question)
        except Exception as exc:
            return AgentResponse(
                answer="Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente em instantes.",
                agent="error",
                used_context=False,
                error=str(exc),
            )

    def _handle_hr_question(self, question: str) -> AgentResponse:
        """Processa perguntas relacionadas a RH (DESABILITADO - Sistema antigo removido)."""

        return AgentResponse(
            answer="Sistema de RH antigo foi desabilitado. Use o SAC Learning GEMS.",
            agent="rh",
            used_context=False,
        )

    def _handle_general_question(self, question: str) -> AgentResponse:
        """Processa perguntas gerais utilizando apenas o LLM."""

        prompt = (
            "Você é um assistente profissional e objetivo."
            " Responda em no máximo duas frases: "
            f"{question}"
        )
        llm_output = self.llm.invoke(prompt)
        answer = getattr(llm_output, "content", llm_output)
        return AgentResponse(
            answer=str(answer).strip(),
            agent="general",
            used_context=False,
        )
