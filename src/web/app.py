"""Aplicação FastAPI para interação web com os agentes."""

from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from ..agents import AgentResponse, AgentService


TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class QuestionPayload(BaseModel):
    """Estrutura do payload enviado pelo frontend."""

    question: str


@lru_cache
def get_agent_service() -> AgentService:
    """Retorna uma instância reutilizável do serviço de agentes."""

    return AgentService()


def create_app() -> FastAPI:
    """Cria e configura a aplicação FastAPI."""

    app = FastAPI(title="Hub de Agentes IA", version="1.0.0")
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def read_home(request: Request) -> HTMLResponse:
        """Retorna a página principal da interface web."""

        return templates.TemplateResponse("index.html", {"request": request})

    @app.post("/api/chat")
    async def chat_endpoint(
        payload: QuestionPayload,
        service: AgentService = Depends(get_agent_service),
    ) -> JSONResponse:
        """Processa uma pergunta enviada pelo usuário."""

        agent_response: AgentResponse = service.answer_question(payload.question)
        status_code = status.HTTP_200_OK if agent_response.error is None else status.HTTP_500_INTERNAL_SERVER_ERROR
        content = {
            "question": payload.question,
            "answer": agent_response.answer,
            "agent": agent_response.agent,
            "used_context": agent_response.used_context,
            "context_preview": agent_response.context_preview,
            "error": agent_response.error,
        }
        return JSONResponse(status_code=status_code, content=content)

    return app


app = create_app()
