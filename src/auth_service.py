"""Serviço de autenticação usando Supabase Auth."""

from typing import Optional, Dict, Any
from datetime import datetime
from .database import get_supabase_client


class AuthService:
    """Gerencia autenticação de usuários via Supabase."""

    def __init__(self):
        self.supabase = get_supabase_client()

    def sign_up(self, email: str, password: str, full_name: str = "") -> Dict[str, Any]:
        """
        Cria uma nova conta de usuário.

        Args:
            email: Email do usuário
            password: Senha (mínimo 6 caracteres)
            full_name: Nome completo do usuário

        Returns:
            Dict com user_id, email e mensagem de sucesso ou erro
        """
        try:
            # Criar usuário no Supabase Auth (sem confirmação de email)
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "email_redirect_to": None,
                    "data": {
                        "full_name": full_name
                    }
                }
            })

            if response.user:
                # Criar registro inicial de subscription (free tier)
                self.supabase.table("subscriptions").insert({
                    "user_id": response.user.id,
                    "status": "free",
                    "plan_name": "free"
                }).execute()

                return {
                    "success": True,
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "message": "Conta criada com sucesso!"
                }
            else:
                return {
                    "success": False,
                    "error": "Erro ao criar conta"
                }

        except Exception as e:
            error_msg = str(e)
            if "already registered" in error_msg.lower():
                error_msg = "Este email já está cadastrado"
            elif "password" in error_msg.lower():
                error_msg = "A senha deve ter no mínimo 6 caracteres"

            return {
                "success": False,
                "error": error_msg
            }

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """
        Realiza login do usuário.

        Args:
            email: Email do usuário
            password: Senha

        Returns:
            Dict com session, user_id, email e access_token ou erro
        """
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if response.user and response.session:
                return {
                    "success": True,
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "full_name": response.user.user_metadata.get("full_name", "")
                }
            else:
                return {
                    "success": False,
                    "error": "Credenciais inválidas"
                }

        except Exception as e:
            error_msg = str(e)
            if "invalid" in error_msg.lower() or "credentials" in error_msg.lower():
                error_msg = "Email ou senha incorretos"

            return {
                "success": False,
                "error": error_msg
            }

    def sign_out(self) -> Dict[str, Any]:
        """
        Realiza logout do usuário.

        Returns:
            Dict com mensagem de sucesso ou erro
        """
        try:
            self.supabase.auth.sign_out()
            return {
                "success": True,
                "message": "Logout realizado com sucesso"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_user_from_token(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Obtém dados do usuário a partir do access token.

        Args:
            access_token: Token de acesso JWT

        Returns:
            Dict com dados do usuário ou None se inválido
        """
        try:
            response = self.supabase.auth.get_user(access_token)
            if response.user:
                return {
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "full_name": response.user.user_metadata.get("full_name", "")
                }
            return None
        except Exception:
            return None

    def verify_session(self, access_token: str) -> bool:
        """
        Verifica se uma sessão é válida.

        Args:
            access_token: Token de acesso JWT

        Returns:
            True se válida, False caso contrário
        """
        user = self.get_user_from_token(access_token)
        return user is not None

    def refresh_session(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """
        Renova a sessão usando refresh token.

        Args:
            refresh_token: Token de refresh

        Returns:
            Dict com novos tokens ou None se falhar
        """
        try:
            response = self.supabase.auth.refresh_session(refresh_token)
            if response.session:
                return {
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token
                }
            return None
        except Exception:
            return None

    def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de assinatura do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Dict com dados da subscription ou None
        """
        try:
            result = self.supabase.table("subscriptions").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()

            if result.data:
                return result.data[0]
            return None
        except Exception:
            return None

    def get_user_usage(self, user_id: str, month_year: Optional[str] = None) -> Dict[str, int]:
        """
        Obtém uso do usuário no mês atual ou especificado.

        Args:
            user_id: ID do usuário
            month_year: Mês/ano no formato 'YYYY-MM' (default: mês atual)

        Returns:
            Dict com contadores de uso
        """
        if not month_year:
            month_year = datetime.now().strftime("%Y-%m")

        try:
            result = self.supabase.table("usage").select("*").eq("user_id", user_id).eq("month_year", month_year).execute()

            if result.data:
                return result.data[0]
            else:
                # Criar registro inicial
                new_usage = {
                    "user_id": user_id,
                    "month_year": month_year,
                    "messages_count": 0,
                    "images_analyzed": 0,
                    "pdfs_analyzed": 0
                }
                self.supabase.table("usage").insert(new_usage).execute()
                return new_usage
        except Exception:
            return {
                "messages_count": 0,
                "images_analyzed": 0,
                "pdfs_analyzed": 0
            }

    def increment_usage(self, user_id: str, usage_type: str) -> bool:
        """
        Incrementa contador de uso.

        Args:
            user_id: ID do usuário
            usage_type: Tipo de uso ('messages_count', 'images_analyzed', 'pdfs_analyzed')

        Returns:
            True se sucesso, False caso contrário
        """
        month_year = datetime.now().strftime("%Y-%m")

        try:
            # Pega ou cria registro de uso
            usage = self.get_user_usage(user_id, month_year)

            # Incrementa contador específico
            current_value = usage.get(usage_type, 0)
            update_data = {
                usage_type: current_value + 1,
                "updated_at": datetime.now().isoformat()
            }

            self.supabase.table("usage").update(update_data).eq("user_id", user_id).eq("month_year", month_year).execute()

            return True
        except Exception:
            return False

    def login_google(self, redirect_url: str = "http://localhost:8001/auth/callback") -> Dict[str, Any]:
        """
        Inicia o fluxo de login com Google OAuth.

        Args:
            redirect_url: URL de callback após autenticação

        Returns:
            Dict com URL de redirecionamento ou erro
        """
        try:
            response = self.supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirect_to": redirect_url
                }
            })

            return {
                "success": True,
                "url": response.url if hasattr(response, 'url') else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def handle_oauth_callback(self, code: str) -> Dict[str, Any]:
        """
        Processa o callback do OAuth (Google).

        Args:
            code: Código de autorização retornado pelo provider

        Returns:
            Dict com session e user_id ou erro
        """
        try:
            # Tentar trocar o código por sessão
            print(f"[DEBUG] Trocando código por sessão: {code[:10]}...")

            response = self.supabase.auth.exchange_code_for_session({
                "auth_code": code
            })

            print(f"[DEBUG] Resposta type: {type(response)}")
            print(f"[DEBUG] Resposta: {response}")

            if hasattr(response, 'session') and hasattr(response, 'user') and response.session and response.user:
                print(f"[DEBUG] Usuário autenticado: {response.user.email}")

                # Verificar se já existe subscription, se não criar
                existing_sub = self.get_user_subscription(response.user.id)

                if not existing_sub:
                    print(f"[DEBUG] Criando subscription para: {response.user.id}")
                    self.supabase.table("subscriptions").insert({
                        "user_id": response.user.id,
                        "status": "free",
                        "plan_name": "free"
                    }).execute()

                return {
                    "success": True,
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token,
                    "full_name": response.user.user_metadata.get("full_name", "")
                }
            else:
                print(f"[DEBUG] Resposta sem session/user")
                return {
                    "success": False,
                    "error": f"Falha na autenticação com Google. Response type: {type(response)}"
                }
        except Exception as e:
            print(f"[DEBUG] Erro no callback: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": f"Erro ao processar callback: {str(e)}"
            }
