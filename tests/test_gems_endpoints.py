"""Testes para os endpoints auxiliares da API web."""

from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.web.app import create_app, get_gem_service
from src.agents import GEMService


def test_history_endpoint():
    """Testa o endpoint /api/history."""
    get_gem_service.cache_clear()
    app = create_app()
    client = TestClient(app)

    # Mock do GEMService
    mock_service = MagicMock(spec=GEMService)
    mock_service.orchestrator.state = {
        "current_gem": "gem2_diagnosticador_foco",
        "completed_gems": ["gem1_mestre_mapeamento"],
        "gem_outputs": {
            "gem1_mestre_mapeamento": {"output": "MAPA-2025-10-001"}
        },
        "gem_conversations": {
            "gem1_mestre_mapeamento": [
                {"role": "user", "content": "mensagem do usuário"},
                {"role": "assistant", "content": "resposta do assistente"}
            ]
        },
        "started_at": "2024-01-01T00:00:00",
        "last_updated": "2024-01-01T01:00:00"
    }
    mock_service.gem_histories = {
        "gem2_diagnosticador_foco": [
            {"role": "system", "content": "instruções do sistema"},
            {"role": "user", "content": "mensagem atual"}
        ]
    }
    mock_service.orchestrator.get_current_gem.return_value = "gem2_diagnosticador_foco"

    # Substitui a dependência
    app.dependency_overrides[get_gem_service] = lambda: mock_service

    response = client.get("/api/history")
    
    assert response.status_code == 200
    data = response.json()
    assert "current_gem" in data
    assert "conversations" in data
    assert "active_history" in data
    assert "completed_gems" in data
    assert data["current_gem"] == "gem2_diagnosticador_foco"
    assert data["completed_gems"] == ["gem1_mestre_mapeamento"]


def test_export_endpoint():
    """Testa o endpoint /api/export."""
    get_gem_service.cache_clear()
    app = create_app()
    client = TestClient(app)

    # Mock do GEMService
    mock_service = MagicMock(spec=GEMService)
    mock_service.orchestrator.state = {
        "current_gem": "gem2_diagnosticador_foco",
        "completed_gems": ["gem1_mestre_mapeamento"],
        "gem_outputs": {
            "gem1_mestre_mapeamento": {
                "output": "MAPA-2025-10-001",
                "completed_at": "2024-01-01T00:00:00"
            }
        },
        "gem_conversations": {
            "gem1_mestre_mapeamento": [
                {"role": "system", "content": "instruções"},
                {"role": "user", "content": "mensagem do usuário"},
                {"role": "assistant", "content": "resposta do assistente"}
            ]
        },
        "started_at": "2024-01-01T00:00:00",
        "last_updated": "2024-01-01T01:00:00"
    }
    mock_service.orchestrator.get_current_gem.return_value = "gem2_diagnosticador_foco"

    # Substitui a dependência
    app.dependency_overrides[get_gem_service] = lambda: mock_service
    
    response = client.get("/api/export")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/markdown"
    assert "Jornada SAC Learning GEMS" in response.text
    assert "MAPA-2025-10-001" in response.text
    assert "Mestre do Mapeamento" in response.text


def test_history_endpoint_with_empty_state():
    """Testa o endpoint /api/history com estado vazio."""
    get_gem_service.cache_clear()
    app = create_app()
    client = TestClient(app)
    
    # Mock do GEMService com estado vazio
    mock_service = MagicMock(spec=GEMService)
    mock_service.orchestrator.state = {
        "current_gem": None,
        "completed_gems": [],
        "gem_outputs": {},
        "gem_conversations": {},
        "started_at": None,
        "last_updated": None
    }
    mock_service.gem_histories = {}
    
    # Substitui a dependência
    app.dependency_overrides[get_gem_service] = lambda: mock_service
    
    response = client.get("/api/history")
    
    assert response.status_code == 200
    data = response.json()
    assert data["current_gem"] is None
    assert data["completed_gems"] == []
    assert data["conversations"] == {}
    assert data["active_history"] is None


def test_export_endpoint_no_completed_gems():
    """Testa o endpoint /api/export quando nenhum GEM foi completado."""
    get_gem_service.cache_clear()
    app = create_app()
    client = TestClient(app)
    
    # Mock do GEMService
    mock_service = MagicMock(spec=GEMService)
    mock_service.orchestrator.state = {
        "current_gem": "gem1_mestre_mapeamento",
        "completed_gems": [],
        "gem_outputs": {},
        "gem_conversations": {},
        "started_at": "2024-01-01T00:00:00",
        "last_updated": "2024-01-01T01:00:00"
    }
    mock_service.orchestrator.get_current_gem.return_value = "gem1_mestre_mapeamento"
    
    # Substitui a dependência
    app.dependency_overrides[get_gem_service] = lambda: mock_service
    
    response = client.get("/api/export")
    
    assert response.status_code == 200
    assert "Nenhum GEM foi completado ainda." in response.text
