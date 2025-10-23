"""Aplicação FastAPI para interação web com o sistema SAC Learning GEMS."""

from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel

from ..agents import GEMService, GEMResponse


TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class MessagePayload(BaseModel):
    """Estrutura do payload enviado pelo frontend."""

    message: str


@lru_cache
def get_gem_service() -> GEMService:
    """Retorna uma instância reutilizável do serviço GEMS."""

    return GEMService(state_file="user_journey_web.json")


def create_app() -> FastAPI:
    """Cria e configura a aplicação FastAPI."""

    app = FastAPI(title="SAC Learning GEMS", version="1.0.0")

    # Adiciona compressão gzip para melhorar performance
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def read_home(request: Request) -> HTMLResponse:
        """Retorna a página principal da interface web."""

        return templates.TemplateResponse("index.html", {"request": request})

    @app.post("/api/chat")
    async def chat_endpoint(
        payload: MessagePayload,
        service: GEMService = Depends(get_gem_service),
    ) -> JSONResponse:
        """Processa uma mensagem enviada pelo usuário."""

        gem_response: GEMResponse = service.process_message(payload.message)
        status_code = status.HTTP_200_OK if gem_response.error is None else status.HTTP_500_INTERNAL_SERVER_ERROR

        content = {
            "message": payload.message,
            "answer": gem_response.answer,
            "gem_id": gem_response.gem_id,
            "gem_name": gem_response.gem_name,
            "is_orchestrator": gem_response.is_orchestrator,
            "error": gem_response.error,
        }
        return JSONResponse(status_code=status_code, content=content)

    @app.get("/api/status")
    async def status_endpoint(
        service: GEMService = Depends(get_gem_service),
    ) -> JSONResponse:
        """Retorna o status atual da jornada do usuário."""

        status_text = service.get_status()
        return JSONResponse(content={"status": status_text})

    @app.post("/api/reset")
    async def reset_endpoint(
        service: GEMService = Depends(get_gem_service),
    ) -> JSONResponse:
        """Reinicia a jornada do usuário."""

        message = service.reset()
        return JSONResponse(content={"message": message})

    return app


app = create_app()
