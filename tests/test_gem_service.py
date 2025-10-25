"""Testes unitários para o GEMService sem acessar APIs externas."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from src.agents import GEMService


class DummyLLM:
    """Simula um LLM necessário pelo serviço."""

    def __init__(self) -> None:
        self.calls = []

    def invoke(self, messages):  # pragma: no cover - caminhos evitados nos testes
        self.calls.append(messages)
        return SimpleNamespace(content="dummy")

    def stream(self, messages):  # pragma: no cover - não usado
        yield SimpleNamespace(content="dummy")


@pytest.fixture()
def temp_state_file(tmp_path: Path) -> Path:
    return tmp_path / "journey.json"


def test_process_message_handles_start_command(temp_state_file: Path) -> None:
    service = GEMService(llm=DummyLLM(), state_file=str(temp_state_file))

    response = service.process_message("iniciar")

    assert response.is_orchestrator is True
    assert "JORNADA INICIADA" in response.answer
    assert response.error is None
    assert service.orchestrator.get_current_gem() == "gem1_mestre_mapeamento"


def test_get_status_before_start(temp_state_file: Path) -> None:
    service = GEMService(llm=DummyLLM(), state_file=str(temp_state_file))

    status = service.get_status()

    assert "Você ainda não iniciou" in status


def test_reset_creates_backup(temp_state_file: Path) -> None:
    service = GEMService(llm=DummyLLM(), state_file=str(temp_state_file))

    service.process_message("iniciar")
    reset_message = service.reset()

    assert "JORNADA REINICIADA" in reset_message
    assert service.orchestrator.get_current_gem() is None
    assert Path(f"{temp_state_file}.backup").exists()
