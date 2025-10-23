"""Aplicação FastAPI para interação web com o sistema SAC Learning GEMS."""

import json
import asyncio
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel

from ..agents import GEMService, GEMResponse
from ..agents.gems import get_all_gems, get_gem_info


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
        gem_info = get_gem_info(gem_id)
        if not gem_info:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "GEM não encontrado"}
            )

        # Atualiza o GEM atual no serviço
        service.activate_gem(gem_id)

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
                yield f"data: {json.dumps({'type': 'start'})}\n\n"
                for chunk in service.process_message_stream(payload.message):
                    event_type = chunk.get("type")

                    if event_type == "chunk":
                        chunk_data = {
                            "type": "chunk",
                            "content": chunk.get("content", ""),
                            "accumulated": chunk.get("accumulated", ""),
                            "gem_id": chunk.get("gem_id"),
                            "gem_name": chunk.get("gem_name"),
                            "is_orchestrator": chunk.get("is_orchestrator", False)
                        }
                        yield f"data: {json.dumps(chunk_data)}\n\n"

                    elif event_type == "done":
                        final_data = {
                            "type": "done",
                            "message": payload.message,
                            "answer": chunk.get("answer", ""),
                            "gem_id": chunk.get("gem_id"),
                            "gem_name": chunk.get("gem_name"),
                            "is_orchestrator": chunk.get("is_orchestrator", False),
                            "error": chunk.get("error")
                        }
                        yield f"data: {json.dumps(final_data)}\n\n"

                    elif event_type == "error":
                        error_data = {
                            "type": "error",
                            "error": chunk.get("error", "Erro desconhecido")
                        }
                        yield f"data: {json.dumps(error_data)}\n\n"

                    await asyncio.sleep(0)

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

    @app.get("/api/history")
    async def history_endpoint(
        service: GEMService = Depends(get_gem_service),
    ) -> JSONResponse:
        """Retorna o histórico de conversas salvo para reconstruir o chat."""

        state = service.orchestrator.state
        current_gem = state.get("current_gem")
        conversations = state.get("gem_conversations", {})
        completed_gems = state.get("completed_gems", [])
        active_history = None

        if current_gem:
            active_history = conversations.get(current_gem)
            if not active_history:
                active_history = service.gem_histories.get(current_gem)

        payload = {
            "current_gem": current_gem,
            "conversations": conversations,
            "active_history": active_history,
            "completed_gems": completed_gems,
        }

        return JSONResponse(content=payload)

    @app.get("/api/export")
    async def export_endpoint(
        service: GEMService = Depends(get_gem_service),
    ) -> StreamingResponse:
        """Exporta a jornada do usuário em formato Markdown."""

        state = service.orchestrator.state
        gem_outputs = state.get("gem_outputs", {})
        gem_conversations = state.get("gem_conversations", {})
        completed_gems = state.get("completed_gems", [])

        lines = ["# Jornada SAC Learning GEMS", ""]

        started_at = state.get("started_at")
        if started_at:
            lines.append(f"- Iniciada em: {started_at}")
        lines.append(f"- Última atualização: {state.get('last_updated', 'não registrado')}")
        lines.append("")

        if completed_gems:
            lines.append("## GEMs Completados")
            lines.append("")

        for gem_id in completed_gems:
            gem_info = get_gem_info(gem_id) or {}
            output = gem_outputs.get(gem_id, {}).get("output", "")

            title = f"{gem_info.get('emoji', '')} {gem_info.get('name', gem_id)}".strip()
            lines.append(f"### {title} ({gem_id})")
            if output:
                lines.append(f"- Output: {output}")
            lines.append("")

            history = gem_conversations.get(gem_id, [])
            if history:
                lines.append("#### Conversa")
                for entry in history:
                    role = entry.get("role", "")
                    content = entry.get("content", "").replace("\r", "")
                    lines.append(f"- **{role.capitalize()}**: {content}")
                lines.append("")

        if not completed_gems:
            lines.append("Nenhum GEM foi completado ainda.")

        content = "\n".join(lines)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jornada-sac-learning-{timestamp}.md"

        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }

        return StreamingResponse(
            iter([content]),
            media_type="text/markdown",
            headers=headers,
        )

    return app


app = create_app()
