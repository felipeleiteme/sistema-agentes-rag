"""Testes unitários para o serviço de agentes."""

import pytest

from src.agents import AgentResponse, AgentService


class DummyLLM:
    """Simula um LLM local para testes."""

    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.prompts = []

    def invoke(self, prompt: str):
        self.prompts.append(prompt)
        return type("LLMResponse", (), {"content": self.reply})()


class DummyKnowledgeTool:
    """Simula a ferramenta de busca na base de conhecimento."""

    def __init__(self, context: str) -> None:
        self.context = context
        self.requests = []

    def _run(self, question: str) -> str:
        self.requests.append(question)
        return self.context


@pytest.fixture
def general_service() -> AgentService:
    return AgentService(llm=DummyLLM("Resposta geral."), knowledge_tool=DummyKnowledgeTool(""))


def test_classify_hr_question(general_service: AgentService) -> None:
    assert general_service.classify_question("Como funcionam as férias?") == "hr"


def test_classify_general_question(general_service: AgentService) -> None:
    assert general_service.classify_question("Qual é a capital do Brasil?") == "general"


def test_hr_question_with_context() -> None:
    llm = DummyLLM("Resposta fundamentada.")
    tool = DummyKnowledgeTool("Contexto relevante sobre férias.")
    service = AgentService(llm=llm, knowledge_tool=tool)

    response = service.answer_question("Quais são as regras de férias?")

    assert isinstance(response, AgentResponse)
    assert response.agent == "rh"
    assert response.used_context is True
    assert response.error is None
    assert "Resposta fundamentada." in response.answer
    assert tool.requests == ["Quais são as regras de férias?"]
    assert len(llm.prompts) == 1


def test_hr_question_without_context() -> None:
    llm = DummyLLM("Outro texto qualquer")
    tool = DummyKnowledgeTool("")
    service = AgentService(llm=llm, knowledge_tool=tool)

    response = service.answer_question("Tenho direito a bônus?")

    assert response.agent == "rh"
    assert response.used_context is False
    assert "Não encontrei informações" in response.answer
    assert response.error is None


def test_general_question_flow() -> None:
    llm = DummyLLM("Capital: Brasília.")
    tool = DummyKnowledgeTool("Qualquer contexto")
    service = AgentService(llm=llm, knowledge_tool=tool)

    response = service.answer_question("Qual é a capital do Brasil?")

    assert response.agent == "general"
    assert response.used_context is False
    assert response.error is None
    assert response.answer == "Capital: Brasília."
