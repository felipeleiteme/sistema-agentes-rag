"""Gerenciamento de conversas e integração com limites."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .database import get_supabase_client
from .limits import check_user_limit, increment_usage

supabase = get_supabase_client()


def create_conversation(user_id: str, title: str = "Nova Conversa") -> Optional[str]:
    """
    Criar nova conversa.

    Args:
        user_id: ID do usuário
        title: Título da conversa

    Returns:
        ID da conversa criada ou None em caso de erro
    """
    try:
        result = supabase.table("conversations").insert({
            "user_id": user_id,
            "title": title
        }).execute()

        if result.data:
            conversation_id = result.data[0]["id"]
            print(f"[DEBUG] Conversa criada: {conversation_id}")
            return conversation_id
        return None

    except Exception as e:
        print(f"[ERROR] Erro ao criar conversa: {e}")
        return None


def save_message(
    conversation_id: str,
    user_id: str,
    role: str,
    content: str
) -> bool:
    """
    Salvar mensagem no histórico.

    Args:
        conversation_id: ID da conversa
        user_id: ID do usuário
        role: 'user' ou 'assistant'
        content: Conteúdo da mensagem

    Returns:
        True se sucesso
    """
    try:
        supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "user_id": user_id,
            "role": role,
            "content": content
        }).execute()

        # Atualizar timestamp da conversa
        supabase.table("conversations").update({
            "updated_at": datetime.now().isoformat()
        }).eq("id", conversation_id).execute()

        print(f"[DEBUG] Mensagem salva: {role} em {conversation_id}")
        return True

    except Exception as e:
        print(f"[ERROR] Erro ao salvar mensagem: {e}")
        return False


def load_conversation_history(conversation_id: str) -> List[Dict[str, Any]]:
    """
    Carregar histórico de mensagens.

    Args:
        conversation_id: ID da conversa

    Returns:
        Lista de mensagens ordenadas por data
    """
    try:
        messages = supabase.table("messages")\
            .select("*")\
            .eq("conversation_id", conversation_id)\
            .order("created_at")\
            .execute()

        return messages.data if messages.data else []

    except Exception as e:
        print(f"[ERROR] Erro ao carregar histórico: {e}")
        return []


def get_or_create_conversation(user_id: str, conversation_id: Optional[str] = None) -> str:
    """
    Obtém uma conversa existente ou cria uma nova.

    Args:
        user_id: ID do usuário
        conversation_id: ID da conversa (opcional)

    Returns:
        ID da conversa
    """
    # Se forneceu ID, verificar se existe e pertence ao usuário
    if conversation_id:
        try:
            conv = supabase.table("conversations")\
                .select("id")\
                .eq("id", conversation_id)\
                .eq("user_id", user_id)\
                .execute()

            if conv.data:
                return conversation_id
        except Exception as e:
            print(f"[ERROR] Erro ao verificar conversa: {e}")

    # Criar nova conversa
    new_id = create_conversation(user_id)
    return new_id if new_id else ""


def update_conversation_title(
    conversation_id: str,
    user_id: str,
    title: str
) -> bool:
    """
    Atualiza o título da conversa.

    Args:
        conversation_id: ID da conversa
        user_id: ID do usuário
        title: Novo título

    Returns:
        True se sucesso
    """
    try:
        result = supabase.table("conversations").update({
            "title": title,
            "updated_at": datetime.now().isoformat()
        }).eq("id", conversation_id).eq("user_id", user_id).execute()

        return bool(result.data)

    except Exception as e:
        print(f"[ERROR] Erro ao atualizar título: {e}")
        return False


def auto_generate_title(conversation_id: str, first_message: str) -> str:
    """
    Gera título automático baseado na primeira mensagem.

    Args:
        conversation_id: ID da conversa
        first_message: Primeira mensagem do usuário

    Returns:
        Título gerado
    """
    # Truncar para 50 caracteres
    title = first_message[:50]
    if len(first_message) > 50:
        title += "..."

    return title


def process_chat_message(
    user_id: str,
    message: str,
    conversation_id: Optional[str] = None,
    agent_processor = None
) -> Dict[str, Any]:
    """
    Processa uma mensagem do chat com verificação de limites.

    Args:
        user_id: ID do usuário
        message: Mensagem do usuário
        conversation_id: ID da conversa (opcional)
        agent_processor: Função que processa a mensagem com o agente

    Returns:
        Dict com resposta ou erro
    """
    try:
        # 1. Verificar limite
        limit_check = check_user_limit(user_id, "messages")
        if not limit_check["allowed"]:
            return {
                "error": True,
                "message": limit_check["message"],
                "upgrade_required": True,
                "remaining": 0,
                "limit": limit_check.get("limit", 50)
            }

        # 2. Obter ou criar conversa
        conv_id = get_or_create_conversation(user_id, conversation_id)
        if not conv_id:
            return {
                "error": True,
                "message": "Erro ao criar conversa"
            }

        # 3. Salvar mensagem do usuário
        save_message(conv_id, user_id, "user", message)

        # 4. Processar com agente (se fornecido)
        if agent_processor:
            response = agent_processor(message)
        else:
            # Resposta padrão se não houver processador
            response = "Agente não configurado. Configure agent_processor."

        # 5. Salvar resposta do assistente
        save_message(conv_id, user_id, "assistant", response)

        # 6. Auto-gerar título se for primeira mensagem
        messages = load_conversation_history(conv_id)
        if len(messages) <= 2:  # user + assistant
            title = auto_generate_title(conv_id, message)
            update_conversation_title(conv_id, user_id, title)

        # 7. Incrementar uso
        increment_usage(user_id, "messages")

        # 8. Retornar sucesso
        return {
            "error": False,
            "response": response,
            "conversation_id": conv_id,
            "remaining": limit_check["remaining"] - 1,
            "limit": limit_check.get("limit", 50),
            "is_premium": limit_check.get("is_premium", False)
        }

    except Exception as e:
        print(f"[ERROR] Erro ao processar chat: {e}")
        import traceback
        traceback.print_exc()
        return {
            "error": True,
            "message": f"Erro ao processar mensagem: {str(e)}"
        }


def delete_conversation(conversation_id: str, user_id: str) -> bool:
    """
    Deleta uma conversa e todas suas mensagens.

    Args:
        conversation_id: ID da conversa
        user_id: ID do usuário

    Returns:
        True se sucesso
    """
    try:
        # Mensagens serão deletadas em cascata pelo banco
        result = supabase.table("conversations")\
            .delete()\
            .eq("id", conversation_id)\
            .eq("user_id", user_id)\
            .execute()

        return bool(result.data)

    except Exception as e:
        print(f"[ERROR] Erro ao deletar conversa: {e}")
        return False


def list_user_conversations(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """
    Lista conversas do usuário.

    Args:
        user_id: ID do usuário
        limit: Número máximo de conversas

    Returns:
        Lista de conversas
    """
    try:
        conversations = supabase.table("conversations")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("updated_at", desc=True)\
            .limit(limit)\
            .execute()

        return conversations.data if conversations.data else []

    except Exception as e:
        print(f"[ERROR] Erro ao listar conversas: {e}")
        return []
