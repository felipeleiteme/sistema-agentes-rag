"""Testes para a app FastAPI com o serviço GEMS."""

from types import SimpleNamespace
from typing import Iterable

from fastapi.testclient import TestClient

from src.agents import GEMResponse
from src.web.app import create_app, get_gem_service


class FakeGEMService:
    """Serviço fake para isolar os endpoints da API."""

    def __init__(
        self,
        response: GEMResponse,
        stream: Iterable[dict] | None = None,
        status_text: str = "",
    ) -> None:
        self._response = response
        self._stream = list(stream or [])
        self._status = status_text
        self.last_message: str | None = None
        self.orchestrator = SimpleNamespace(
            get_current_gem=lambda: "gem1_mestre_mapeamento",
            state={},
        )

    def process_message(self, message: str) -> GEMResponse:
        self.last_message = message
        return self._response

    def process_message_stream(self, message: str):  # pragma: no cover - generator
        for chunk in self._stream:
            yield chunk

    def get_status(self) -> str:
        return self._status

    def activate_gem(self, gem_id: str) -> str:  # pragma: no cover - não usado
        return f"Ativado: {gem_id}"

    def reset(self) -> str:  # pragma: no cover - não usado
        return "Resetado"


def build_client(service: FakeGEMService) -> tuple[TestClient, FakeGEMService]:
    get_gem_service.cache_clear()
    app = create_app()
    app.dependency_overrides[get_gem_service] = lambda: service
    return TestClient(app), service


def test_home_page_renders_template() -> None:
    client, _ = build_client(
        FakeGEMService(GEMResponse(answer="", gem_id=None, gem_name=None, is_orchestrator=True))
    )
    response = client.get("/")
    assert response.status_code == 200
    assert "SAC Learning GEMS" in response.text


def test_chat_endpoint_returns_payload() -> None:
    expected = GEMResponse(
        answer="Resposta de teste",
        gem_id="gem1_mestre_mapeamento",
        gem_name="Mestre do Mapeamento",
        is_orchestrator=False,
        error=None,
    )
    client, service = build_client(FakeGEMService(expected))

    response = client.post("/api/chat", json={"message": "iniciar"})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == expected.answer
    assert body["gem_id"] == expected.gem_id
    assert body["gem_name"] == expected.gem_name
    assert body["is_orchestrator"] is expected.is_orchestrator
    assert service.last_message == "iniciar"


def test_status_endpoint_returns_service_status() -> None:
    status_text = "Status atual"
    client, _ = build_client(
        FakeGEMService(
            GEMResponse(answer="", gem_id=None, gem_name=None, is_orchestrator=True),
            status_text=status_text,
        )
    )

    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"status": status_text}


def test_chat_stream_endpoint_streams_chunks() -> None:
    stream = [
        {
            "type": "chunk",
            "content": "Olá",
            "accumulated": "Olá",
            "gem_id": "gem1_mestre_mapeamento",
            "gem_name": "Mestre do Mapeamento",
            "is_orchestrator": False,
        },
        {
            "type": "done",
            "message": "iniciar",
            "answer": "Olá",
            "gem_id": "gem1_mestre_mapeamento",
            "gem_name": "Mestre do Mapeamento",
            "is_orchestrator": False,
            "error": None,
        },
    ]

    client, _ = build_client(
        FakeGEMService(
            GEMResponse(answer="", gem_id=None, gem_name=None, is_orchestrator=True),
            stream=stream,
        )
    )

    response = client.post("/api/chat/stream", json={"message": "iniciar"})

    assert response.status_code == 200
    body = b"".join(response.iter_bytes())
    assert b"data: {\"type\": \"chunk\"" in body
    assert b"data: {\"type\": \"done\"" in body
