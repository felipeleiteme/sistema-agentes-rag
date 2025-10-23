"""Aplicação FastAPI para interação web com o sistema SAC Learning GEMS."""

from functools import lru_cache
from pathlib import Path
import json
import asyncio

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
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

    @app.get("/api/gems")
    async def list_gems_endpoint(
        service: GEMService = Depends(get_gem_service),
    ) -> JSONResponse:
        """Lista todos os GEMs disponíveis e o GEM atual."""
        from ..agents.gems import get_all_gems

        all_gems = get_all_gems()
        current_gem = service.orchestrator.get_current_gem()

        return JSONResponse(content={
            "gems": all_gems,
            "current_gem": current_gem
        })

    @app.post("/api/gems/{gem_id}/activate")
    async def activate_gem_endpoint(
        gem_id: str,
        service: GEMService = Depends(get_gem_service),
    ) -> JSONResponse:
        """Permite navegar livremente para qualquer GEM."""
        from ..agents.gems import get_gem_info

        gem_info = get_gem_info(gem_id)
        if not gem_info:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "GEM não encontrado"}
            )

        # Atualiza o GEM atual no orquestrador
        service.orchestrator.current_gem = gem_id
        service.orchestrator._save_state()

        return JSONResponse(content={
            "message": f"Navegado para {gem_info['name']} {gem_info['emoji']}",
            "gem_id": gem_id,
            "gem_name": gem_info['name']
        })

    @app.post("/api/reset")
    async def reset_endpoint(
        service: GEMService = Depends(get_gem_service),
    ) -> JSONResponse:
        """Reinicia a jornada do usuário."""

        message = service.reset()
        return JSONResponse(content={"message": message})

    @app.post("/api/chat/stream")
    async def chat_stream_endpoint(
        payload: MessagePayload,
        service: GEMService = Depends(get_gem_service),
    ) -> StreamingResponse:
        """Processa uma mensagem com streaming de resposta."""

        async def event_generator():
            try:
                # Processa a mensagem de forma síncrona (por enquanto)
                # Em uma implementação real, você precisaria fazer o streaming
                # diretamente do LLM, mas isso requer modificações profundas

                # Envia evento de início
                yield f"data: {json.dumps({'type': 'start'})}\n\n"
                await asyncio.sleep(0.1)

                # Processa mensagem
                gem_response: GEMResponse = service.process_message(payload.message)

                # Simula streaming da resposta palavra por palavra para melhor UX
                words = gem_response.answer.split()
                accumulated = ""

                for i, word in enumerate(words):
                    accumulated += word + " "
                    chunk_data = {
                        "type": "chunk",
                        "content": word + " ",
                        "accumulated": accumulated.strip(),
                        "gem_id": gem_response.gem_id,
                        "gem_name": gem_response.gem_name,
                        "is_orchestrator": gem_response.is_orchestrator
                    }
                    yield f"data: {json.dumps(chunk_data)}\n\n"
                    # Delay adaptativo: mais rápido no início, mais lento depois
                    delay = 0.03 if i < 10 else 0.02
                    await asyncio.sleep(delay)

                # Envia evento de conclusão
                final_data = {
                    "type": "done",
                    "message": payload.message,
                    "answer": gem_response.answer,
                    "gem_id": gem_response.gem_id,
                    "gem_name": gem_response.gem_name,
                    "is_orchestrator": gem_response.is_orchestrator,
                    "error": gem_response.error
                }
                yield f"data: {json.dumps(final_data)}\n\n"

            except Exception as e:
                error_data = {
                    "type": "error",
                    "error": str(e)
                }
                yield f"data: {json.dumps(error_data)}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            }
        )

    return app


app = create_app()
