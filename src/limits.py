"""Sistema de limites de uso para free tier e premium."""

from typing import Dict, Any
from datetime import datetime
from .database import get_supabase_client

supabase = get_supabase_client()

# Limites do plano gratuito
FREE_TIER_LIMITS = {
    "messages_per_month": 50,
    "images_per_month": 5,
    "pdfs_per_month": 2
}


def check_user_limit(user_id: str, limit_type: str = "messages") -> Dict[str, Any]:
    """
    Verifica se usuário pode usar o recurso.

    Args:
        user_id: ID do usuário
        limit_type: Tipo de limite ('messages', 'images', 'pdfs')

    Returns:
        Dict com informações sobre o limite
    """
    try:
        # 1. Buscar assinatura do usuário
        subscription = supabase.table("subscriptions")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()

        # Se não tem subscription, criar uma free
        if not subscription.data:
            supabase.table("subscriptions").insert({
                "user_id": user_id,
                "status": "free",
                "plan_name": "free"
            }).execute()
            subscription_status = "free"
        else:
            subscription_status = subscription.data[0]["status"]

        # Se premium/active, sem limites
        if subscription_status == "active":
            return {
                "allowed": True,
                "remaining": "unlimited",
                "plan": "premium",
                "is_premium": True
            }

        # Se free, verificar uso mensal
        current_month = datetime.now().strftime("%Y-%m")

        usage = supabase.table("usage")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("month_year", current_month)\
            .execute()

        if not usage.data:
            # Primeiro uso do mês, criar registro
            supabase.table("usage").insert({
                "user_id": user_id,
                "month_year": current_month,
                "messages_count": 0,
                "images_analyzed": 0,
                "pdfs_analyzed": 0
            }).execute()
            current_usage = 0
        else:
            # Mapear tipo de limite para campo do banco
            field_name = f"{limit_type}_count" if limit_type == "messages" else f"{limit_type}_analyzed"
            current_usage = usage.data[0].get(field_name, 0)

        # Obter limite máximo
        limit_name = f"{limit_type}_per_month"
        max_limit = FREE_TIER_LIMITS.get(limit_name, 50)

        # Verificar se atingiu o limite
        if current_usage >= max_limit:
            return {
                "allowed": False,
                "remaining": 0,
                "current_usage": current_usage,
                "limit": max_limit,
                "plan": "free",
                "is_premium": False,
                "message": f"Limite de {max_limit} {limit_type}/mês atingido. Faça upgrade para continuar!"
            }

        return {
            "allowed": True,
            "remaining": max_limit - current_usage,
            "current_usage": current_usage,
            "limit": max_limit,
            "plan": "free",
            "is_premium": False
        }

    except Exception as e:
        print(f"[ERROR] Erro ao verificar limite: {e}")
        # Em caso de erro, permitir (fallback seguro)
        return {
            "allowed": True,
            "remaining": "unknown",
            "plan": "free",
            "is_premium": False,
            "error": str(e)
        }


def increment_usage(user_id: str, usage_type: str = "messages") -> bool:
    """
    Incrementa contador de uso.

    Args:
        user_id: ID do usuário
        usage_type: Tipo de uso ('messages', 'images', 'pdfs')

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        current_month = datetime.now().strftime("%Y-%m")

        # Mapear tipo de uso para campo do banco
        field_name = f"{usage_type}_count" if usage_type == "messages" else f"{usage_type}_analyzed"

        # Usar função SQL para incrementar
        result = supabase.rpc("increment_usage", {
            "p_user_id": user_id,
            "p_month_year": current_month,
            "p_field": field_name
        }).execute()

        print(f"[DEBUG] Incrementado uso de {usage_type} para usuário {user_id}")
        return True

    except Exception as e:
        print(f"[ERROR] Erro ao incrementar uso: {e}")
        return False


def get_usage_stats(user_id: str) -> Dict[str, Any]:
    """
    Obtém estatísticas de uso do usuário no mês atual.

    Args:
        user_id: ID do usuário

    Returns:
        Dict com estatísticas de uso
    """
    try:
        current_month = datetime.now().strftime("%Y-%m")

        usage = supabase.table("usage")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("month_year", current_month)\
            .execute()

        if not usage.data:
            return {
                "messages_count": 0,
                "images_analyzed": 0,
                "pdfs_analyzed": 0,
                "messages_remaining": FREE_TIER_LIMITS["messages_per_month"],
                "images_remaining": FREE_TIER_LIMITS["images_per_month"],
                "pdfs_remaining": FREE_TIER_LIMITS["pdfs_per_month"]
            }

        data = usage.data[0]
        return {
            "messages_count": data.get("messages_count", 0),
            "images_analyzed": data.get("images_analyzed", 0),
            "pdfs_analyzed": data.get("pdfs_analyzed", 0),
            "messages_remaining": FREE_TIER_LIMITS["messages_per_month"] - data.get("messages_count", 0),
            "images_remaining": FREE_TIER_LIMITS["images_per_month"] - data.get("images_analyzed", 0),
            "pdfs_remaining": FREE_TIER_LIMITS["pdfs_per_month"] - data.get("pdfs_analyzed", 0)
        }

    except Exception as e:
        print(f"[ERROR] Erro ao obter estatísticas: {e}")
        return {
            "messages_count": 0,
            "images_analyzed": 0,
            "pdfs_analyzed": 0,
            "error": str(e)
        }


def reset_monthly_usage(user_id: str) -> bool:
    """
    Reseta o uso mensal (útil para testes ou admin).

    Args:
        user_id: ID do usuário

    Returns:
        True se sucesso
    """
    try:
        current_month = datetime.now().strftime("%Y-%m")

        supabase.table("usage")\
            .update({
                "messages_count": 0,
                "images_analyzed": 0,
                "pdfs_analyzed": 0
            })\
            .eq("user_id", user_id)\
            .eq("month_year", current_month)\
            .execute()

        print(f"[DEBUG] Uso resetado para usuário {user_id}")
        return True

    except Exception as e:
        print(f"[ERROR] Erro ao resetar uso: {e}")
        return False
