"""Testes para a API web baseada em FastAPI."""

from fastapi.testclient import TestClient

from src.agents import AgentResponse
from src.web.app import create_app, get_agent_service


class FakeAgentService:
    """Mock do serviço de agentes usado durante os testes da API."""

    def __init__(self, response: AgentResponse) -> None:
        self.response = response
        self.calls = []

    def answer_question(self, question: str) -> AgentResponse:
        self.calls.append(question)
        return self.response


def build_client(response: AgentResponse) -> tuple[TestClient, FakeAgentService]:
    get_agent_service.cache_clear()
    app = create_app()
    fake_service = FakeAgentService(response)
    app.dependency_overrides[get_agent_service] = lambda: fake_service
    return TestClient(app), fake_service


def test_home_page_loads() -> None:
    client, _ = build_client(
        AgentResponse(answer="Olá", agent="general", used_context=False)
    )
    res = client.get("/")
    assert res.status_code == 200
    assert "Hub de Agentes IA" in res.text


def test_chat_endpoint_returns_answer() -> None:
    client, service = build_client(
        AgentResponse(answer="Resposta teste", agent="rh", used_context=True, context_preview="trecho")
    )
    res = client.post("/api/chat", json={"question": "Como funcionam as férias?"})
    assert res.status_code == 200
    data = res.json()
    assert data["answer"] == "Resposta teste"
    assert data["agent"] == "rh"
    assert data["used_context"] is True
    assert service.calls == ["Como funcionam as férias?"]


def test_chat_endpoint_handles_error() -> None:
    client, _ = build_client(
        AgentResponse(
            answer="Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente em instantes.",
            agent="error",
            used_context=False,
            error="Falha de conexão",
        )
    )
    res = client.post("/api/chat", json={"question": "Pergunta qualquer"})
    assert res.status_code == 500
    assert res.json()["error"] == "Falha de conexão"
