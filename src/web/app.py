"""Aplicação FastAPI para interação web com o sistema SAC Learning GEMS."""

import json
import asyncio
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Request, status, Cookie, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel

from ..agents import GEMService, GEMResponse
from ..agents.gems import get_all_gems, get_gem_info
from ..auth_service import AuthService
from ..database import get_supabase_client
from ..limits import check_user_limit, get_usage_stats
from ..chat_manager import process_chat_message, save_message


TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
STATIC_DIR = Path(__file__).resolve().parent / "static"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class MessagePayload(BaseModel):
    """Estrutura do payload enviado pelo frontend."""

    message: str


class LoginPayload(BaseModel):
    """Estrutura do payload de login."""

    email: str
    password: str


class RegisterPayload(BaseModel):
    """Estrutura do payload de registro."""

    email: str
    password: str
    full_name: str = ""


@lru_cache
def get_gem_service() -> GEMService:
    """Retorna uma instância reutilizável do serviço GEMS."""

    return GEMService(state_file="user_journey_web.json")


@lru_cache
def get_auth_service() -> AuthService:
    """Retorna uma instância reutilizável do serviço de autenticação."""

    return AuthService()


async def get_current_user(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service)
) -> Optional[dict]:
    """
    Obtém o usuário atual a partir do token no header Authorization.
    Retorna None se não autenticado.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    user = auth_service.get_user_from_token(token)
    return user


async def require_auth(
    user: Optional[dict] = Depends(get_current_user)
) -> dict:
    """
    Dependency que requer autenticação.
    Lança HTTPException se usuário não estiver autenticado.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado"
        )
    return user


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

    @app.get("/login", response_class=HTMLResponse)
    async def login_page(request: Request) -> HTMLResponse:
        """Retorna a página de login."""

        return templates.TemplateResponse("login.html", {"request": request})

    @app.get("/register", response_class=HTMLResponse)
    async def register_page(request: Request) -> HTMLResponse:
        """Retorna a página de registro."""

        return templates.TemplateResponse("register.html", {"request": request})

    @app.post("/api/auth/register")
    async def register_endpoint(
        payload: RegisterPayload,
        auth_service: AuthService = Depends(get_auth_service),
    ) -> JSONResponse:
        """Cria uma nova conta de usuário."""

        result = auth_service.sign_up(
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name
        )

        return JSONResponse(content=result)

    @app.post("/api/auth/login")
    async def login_endpoint(
        payload: LoginPayload,
        auth_service: AuthService = Depends(get_auth_service),
    ) -> JSONResponse:
        """Realiza login do usuário."""

        result = auth_service.sign_in(
            email=payload.email,
            password=payload.password
        )

        return JSONResponse(content=result)

    @app.post("/api/auth/logout")
    async def logout_endpoint(
        auth_service: AuthService = Depends(get_auth_service),
    ) -> JSONResponse:
        """Realiza logout do usuário."""

        result = auth_service.sign_out()
        return JSONResponse(content=result)

    @app.get("/api/auth/me")
    async def me_endpoint(
        user: dict = Depends(require_auth),
        auth_service: AuthService = Depends(get_auth_service),
    ) -> JSONResponse:
        """Retorna informações do usuário autenticado."""

        # Buscar subscription do usuário
        subscription = auth_service.get_user_subscription(user["user_id"])
        usage = auth_service.get_user_usage(user["user_id"])

        return JSONResponse(content={
            **user,
            "subscription": subscription,
            "usage": usage
        })

    @app.get("/api/auth/google")
    async def google_login_endpoint(
        auth_service: AuthService = Depends(get_auth_service),
    ) -> JSONResponse:
        """Inicia o fluxo de login com Google."""

        result = auth_service.login_google()
        return JSONResponse(content=result)

    @app.get("/auth/callback")
    async def auth_callback_endpoint(
        code: str,
        auth_service: AuthService = Depends(get_auth_service),
    ) -> HTMLResponse:
        """Callback do OAuth (Google) - processa o código e redireciona."""

        try:
            result = auth_service.handle_oauth_callback(code)

            # Verificar se result é um dicionário
            if not isinstance(result, dict):
                error_msg = f"Resposta inválida do servidor: {result}"
            elif result.get("success"):
                # Criar página HTML que salva tokens e redireciona
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Autenticando...</title>
                </head>
                <body>
                    <script>
                        // Salvar tokens no localStorage
                        localStorage.setItem('access_token', '{result["access_token"]}');
                        localStorage.setItem('refresh_token', '{result["refresh_token"]}');
                        localStorage.setItem('user_email', '{result["email"]}');
                        localStorage.setItem('user_id', '{result["user_id"]}');

                        // Redirecionar para home
                        window.location.href = '/';
                    </script>
                    <p>Autenticando... Você será redirecionado em instantes.</p>
                </body>
                </html>
                """
                return HTMLResponse(content=html_content)
            else:
                error_msg = result.get('error', 'Erro desconhecido')

        except Exception as e:
            error_msg = f"Erro no callback: {str(e)}"

        # Erro na autenticação
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Erro na autenticação</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 2rem; max-width: 600px; margin: 0 auto; }}
                h1 {{ color: #dc2626; }}
                .error {{ background: #fef2f2; border: 1px solid #fecaca; padding: 1rem; border-radius: 8px; margin: 1rem 0; }}
                a {{ color: #667eea; text-decoration: none; font-weight: 600; }}
            </style>
        </head>
        <body>
            <h1>Erro ao autenticar com Google</h1>
            <div class="error">
                <p><strong>Detalhes do erro:</strong></p>
                <p>{error_msg}</p>
            </div>
            <p><a href="/login">← Voltar para login</a></p>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    @app.get("/api/usage")
    async def usage_endpoint(
        user: dict = Depends(require_auth),
    ) -> JSONResponse:
        """Retorna estatísticas de uso do usuário."""

        stats = get_usage_stats(user["user_id"])
        return JSONResponse(content=stats)

    @app.post("/api/chat")
    async def chat_endpoint(
        payload: MessagePayload,
        service: GEMService = Depends(get_gem_service),
        user: Optional[dict] = Depends(get_current_user),
    ) -> JSONResponse:
        """Processa uma mensagem enviada pelo usuário."""

        # Se usuário autenticado, verificar limites
        if user:
            limit_check = check_user_limit(user["user_id"], "messages")

            # Bloquear se atingiu o limite
            if not limit_check["allowed"]:
                return JSONResponse(
                    status_code=status.HTTP_402_PAYMENT_REQUIRED,
                    content={
                        "error": "limit_exceeded",
                        "message": limit_check["message"],
                        "remaining": 0,
                        "limit": limit_check.get("limit", 50),
                        "upgrade_required": True
                    }
                )

        # Processar mensagem normalmente
        gem_response: GEMResponse = service.process_message(payload.message)
        status_code = status.HTTP_200_OK if gem_response.error is None else status.HTTP_500_INTERNAL_SERVER_ERROR

        # Se usuário autenticado, usar chat_manager para salvar
        if user and not gem_response.error:
            # Incrementar uso através do chat_manager
            # (já incrementa automaticamente no process_chat_message)
            from ..limits import increment_usage
            increment_usage(user["user_id"], "messages")

        content = {
            "message": payload.message,
            "answer": gem_response.answer,
            "gem_id": gem_response.gem_id,
            "gem_name": gem_response.gem_name,
            "is_orchestrator": gem_response.is_orchestrator,
            "error": gem_response.error,
        }

        # Adicionar informações de limite se autenticado
        if user:
            limit_check = check_user_limit(user["user_id"], "messages")
            content["remaining"] = limit_check.get("remaining", "unknown")
            content["is_premium"] = limit_check.get("is_premium", False)

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
                yield f"data: {json.dumps({'type': 'start'}, ensure_ascii=False)}\n\n"
                for chunk in service.process_message_stream(payload.message):
                    event_type = chunk.get("type")

                    if event_type == "chunk":
                        chunk_data = {
                            "type": "chunk",
                            "content": str(chunk.get("content", "")),
                            "accumulated": str(chunk.get("accumulated", "")),
                            "gem_id": chunk.get("gem_id"),
                            "gem_name": chunk.get("gem_name"),
                            "is_orchestrator": chunk.get("is_orchestrator", False)
                        }
                        yield f"data: {json.dumps(chunk_data, ensure_ascii=False)}\n\n"

                    elif event_type == "done":
                        final_data = {
                            "type": "done",
                            "message": str(payload.message),
                            "answer": str(chunk.get("answer", "")),
                            "gem_id": chunk.get("gem_id"),
                            "gem_name": chunk.get("gem_name"),
                            "is_orchestrator": chunk.get("is_orchestrator", False),
                            "error": chunk.get("error")
                        }
                        yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"

                    elif event_type == "error":
                        error_data = {
                            "type": "error",
                            "error": str(chunk.get("error", "Erro desconhecido"))
                        }
                        yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"

                    await asyncio.sleep(0)

            except Exception as e:
                error_data = {
                    "type": "error",
                    "error": str(e)
                }
                yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
            }
        )

    # ========== ROTAS DE GERENCIAMENTO DE CONVERSAS ==========

    @app.get("/api/conversations")
    async def list_conversations_endpoint(
        user: dict = Depends(require_auth),
    ) -> JSONResponse:
        """Lista todas as conversas do usuário autenticado."""

        supabase = get_supabase_client()
        result = supabase.table("conversations").select("*").eq("user_id", user["user_id"]).order("updated_at", desc=True).execute()

        return JSONResponse(content={"conversations": result.data})

    @app.post("/api/conversations")
    async def create_conversation_endpoint(
        user: dict = Depends(require_auth),
    ) -> JSONResponse:
        """Cria uma nova conversa."""

        supabase = get_supabase_client()
        result = supabase.table("conversations").insert({
            "user_id": user["user_id"],
            "title": "Nova Conversa"
        }).execute()

        return JSONResponse(content={"conversation": result.data[0]})

    @app.get("/api/conversations/{conversation_id}")
    async def get_conversation_endpoint(
        conversation_id: str,
        user: dict = Depends(require_auth),
    ) -> JSONResponse:
        """Obtém uma conversa específica com suas mensagens."""

        supabase = get_supabase_client()

        # Verificar se a conversa pertence ao usuário
        conv_result = supabase.table("conversations").select("*").eq("id", conversation_id).eq("user_id", user["user_id"]).execute()

        if not conv_result.data:
            raise HTTPException(status_code=404, detail="Conversa não encontrada")

        # Buscar mensagens da conversa
        messages_result = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()

        return JSONResponse(content={
            "conversation": conv_result.data[0],
            "messages": messages_result.data
        })

    @app.put("/api/conversations/{conversation_id}")
    async def update_conversation_endpoint(
        conversation_id: str,
        title: str,
        user: dict = Depends(require_auth),
    ) -> JSONResponse:
        """Atualiza o título de uma conversa."""

        supabase = get_supabase_client()

        result = supabase.table("conversations").update({
            "title": title,
            "updated_at": datetime.now().isoformat()
        }).eq("id", conversation_id).eq("user_id", user["user_id"]).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Conversa não encontrada")

        return JSONResponse(content={"conversation": result.data[0]})

    @app.delete("/api/conversations/{conversation_id}")
    async def delete_conversation_endpoint(
        conversation_id: str,
        user: dict = Depends(require_auth),
    ) -> JSONResponse:
        """Deleta uma conversa e suas mensagens."""

        supabase = get_supabase_client()

        # Deletar conversa (mensagens serão deletadas em cascata)
        result = supabase.table("conversations").delete().eq("id", conversation_id).eq("user_id", user["user_id"]).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Conversa não encontrada")

        return JSONResponse(content={"message": "Conversa deletada com sucesso"})

    @app.post("/api/conversations/{conversation_id}/messages")
    async def save_message_endpoint(
        conversation_id: str,
        role: str,
        content: str,
        user: dict = Depends(require_auth),
    ) -> JSONResponse:
        """Salva uma mensagem em uma conversa."""

        supabase = get_supabase_client()

        # Verificar se a conversa existe e pertence ao usuário
        conv_result = supabase.table("conversations").select("id").eq("id", conversation_id).eq("user_id", user["user_id"]).execute()

        if not conv_result.data:
            raise HTTPException(status_code=404, detail="Conversa não encontrada")

        # Criar mensagem
        message_result = supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "user_id": user["user_id"],
            "role": role,
            "content": content
        }).execute()

        # Atualizar timestamp da conversa
        supabase.table("conversations").update({
            "updated_at": datetime.now().isoformat()
        }).eq("id", conversation_id).execute()

        return JSONResponse(content={"message": message_result.data[0]})

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
