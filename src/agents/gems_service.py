"""
Serviço principal do Sistema SAC Learning GEMS.
Integra o orquestrador com os agentes GEM especializados.
"""

from dataclasses import dataclass
from typing import Dict, Generator, Optional, Any, List, Tuple
from langchain_ollama import ChatOllama

from ..config import GEMConfig
from .orchestrator import GEMOrchestrator
from .gems import get_gem_info


@dataclass
class GEMResponse:
    """Representa a resposta do sistema GEMS."""

    answer: str
    gem_id: Optional[str] = None
    gem_name: Optional[str] = None
    is_orchestrator: bool = False
    error: Optional[str] = None


class GEMService:
    """
    Serviço principal que gerencia a interação do usuário com os GEMs.

    Responsabilidades:
    - Gerenciar estado da jornada via orquestrador
    - Processar comandos do sistema
    - Rotear mensagens para o GEM apropriado
    - Compartilhar contexto entre GEMs para personalização
    """

    def __init__(
        self,
        llm: Optional[ChatOllama] = None,
        state_file: str = "user_journey.json"
    ):
        """
        Inicializa o serviço GEMS.

        Args:
            llm: Instância do LLM (padrão: Ollama llama3.2:3b)
            state_file: Arquivo para persistir estado da jornada
        """
        # Configuração otimizada do LLM para velocidade máxima
        llm_config = GEMConfig.get_llm_config()
        self.llm = llm or ChatOllama(**llm_config)

        self.orchestrator = GEMOrchestrator(state_file=state_file)

        # Histórico de mensagens por GEM durante a sessão
        self.gem_histories: Dict[str, List[Dict[str, str]]] = {}

        # Dicionário de comandos e seus métodos correspondentes
        self._command_registry = {
            "/concluir": self._handle_completion_command,
            "/finalizar": self._handle_completion_command, 
            "/finalize": self._handle_completion_command,
        }
        
        # Conjunto de comandos de força de conclusão para verificação rápida
        self._force_completion_commands = set(self._command_registry.keys())

    def _handle_completion_command(self, user_message: str) -> bool:
        """Lida com o comando de conclusão forçada."""
        return True  # Retorna True para indicar que é um comando de conclusão

    def process_message(self, user_message: str) -> GEMResponse:
        """
        Processa uma mensagem do usuário.

        Args:
            user_message: Mensagem enviada pelo usuário

        Returns:
            GEMResponse com a resposta apropriada
        """
        try:
            # Primeiro, tenta processar como comando do orquestrador
            response, gem_id = self.orchestrator.handle_command(user_message)

            if response:
                # É um comando do sistema
                return GEMResponse(
                    answer=response,
                    is_orchestrator=True
                )

            # Não é comando, processa com o GEM atual
            current_gem = self.orchestrator.get_current_gem()

            if not current_gem:
                # Nenhum GEM ativo, sugere iniciar
                return GEMResponse(
                    answer=self.orchestrator.get_welcome_message(),
                    is_orchestrator=True
                )

            # Processa com o GEM atual
            return self._handle_gem_interaction(current_gem, user_message)

        except Exception as e:
            return GEMResponse(
                answer="Desculpe, ocorreu um erro. Tente novamente.",
                error=str(e)
            )

    def process_message_stream(self, user_message: str) -> Generator[Dict[str, Any], None, None]:
        """Processa uma mensagem retornando chunks de resposta em streaming."""
        try:
            response, gem_id = self.orchestrator.handle_command(user_message)

            if response:
                yield {
                    "type": "chunk",
                    "content": response,
                    "accumulated": response,
                    "gem_id": gem_id,
                    "gem_name": None,
                    "is_orchestrator": True,
                }
                yield {
                    "type": "done",
                    "message": user_message,
                    "answer": response,
                    "gem_id": gem_id,
                    "gem_name": None,
                    "is_orchestrator": True,
                    "error": None,
                }
                return

            current_gem = self.orchestrator.get_current_gem()

            if not current_gem:
                welcome = self.orchestrator.get_welcome_message()
                yield {
                    "type": "chunk",
                    "content": welcome,
                    "accumulated": welcome,
                    "gem_id": None,
                    "gem_name": None,
                    "is_orchestrator": True,
                }
                yield {
                    "type": "done",
                    "message": user_message,
                    "answer": welcome,
                    "gem_id": None,
                    "gem_name": None,
                    "is_orchestrator": True,
                    "error": None,
                }
                return

            gem_response = self._stream_gem_interaction(current_gem, user_message)
            yield from gem_response

        except Exception as e:  # pylint: disable=broad-except
            yield {
                "type": "error",
                "error": str(e),
            }

    def _handle_gem_interaction(self, gem_id: str, user_message: str) -> GEMResponse:
        """
        Processa interação com um GEM específico.

        Args:
            gem_id: ID do GEM
            user_message: Mensagem do usuário

        Returns:
            GEMResponse com resposta do GEM
        """
        gem_info = get_gem_info(gem_id)

        try:
            force_completion = self._is_force_completion_command(user_message)

            self._ensure_gem_history(gem_id, gem_info)
            self._append_user_message(gem_id, user_message, gem_info, force_completion)

            messages = self.gem_histories[gem_id]

            response = self.llm.invoke(messages)
            answer = getattr(response, "content", str(response)).strip()

            self._append_assistant_response(gem_id, answer)

            final_answer, _ = self._finalize_interaction(gem_id, answer, gem_info, force_completion)

            return GEMResponse(
                answer=final_answer,
                gem_id=gem_id,
                gem_name=gem_info['name']
            )

        except Exception as e:  # pylint: disable=broad-except
            return GEMResponse(
                answer=f"Erro ao processar com {gem_info['name']}: {str(e)}",
                gem_id=gem_id,
                gem_name=gem_info['name'],
                error=str(e)
            )

    def _is_gem_complete(self, response: str, gem_id: str) -> bool:
        """
        Detecta se um GEM completou sua tarefa.

        Args:
            response: Resposta do GEM
            gem_id: ID do GEM

        Returns:
            True se o GEM completou
        """
        # Padrões primários de IDs gerados pelos GEMs
        completion_patterns = {
            "gem1_mestre_mapeamento": "MAPA-",
            "gem2_diagnosticador_foco": "FOCO-",
            "gem3_validador_estrategico": "RESULTADO DA VALIDAÇÃO",
            "gem4_laboratorio_cientifico": "METODO-",
            "gem5_tutor_socratico": "CERTIFICAÇÃO",
            "gem6_arquiteto_implementacao": "PLANO-",
            "gem7_construtor_sistemas": "KBF-"
        }

        pattern = completion_patterns.get(gem_id, "")
        if pattern and pattern in response:
            return True

        # Detecção secundária: padrões de finalização
        response_lower = response.lower()

        # GEM 1 - Sinais de que completou o mapeamento
        if gem_id == "gem1_mestre_mapeamento":
            gem1_completion_signals = [
                "sua sessão com o mestre do mapeamento está completa",
                "mapeamento m.a.p.a. completo",
                "id do mapeamento",
                "próximo agente" in response_lower and "diagnosticador f.o.c.o" in response_lower
            ]
            if any(gem1_completion_signals):
                return True

            # Verifica se há histórico suficiente para forçar conclusão
            if gem_id in self.gem_histories:
                history_length = len([m for m in self.gem_histories[gem_id] if m["role"] == "assistant"])
                # Se já trocou mais de 8 mensagens e menciona "pronto" ou "avançar", força conclusão
                if history_length >= 8 and ("pronto para avançar" in response_lower or "está pronto" in response_lower):
                    return True

        return False

    def _extract_gem_output(self, response: str, gem_id: str) -> str:
        """
        Extrai o output estruturado de um GEM.

        Args:
            response: Resposta completa do GEM
            gem_id: ID do GEM

        Returns:
            Output estruturado (ex: "MAPA-2025-10-001")
        """
        # Implementação básica: pega a primeira linha que contém o ID
        lines = response.split('\n')
        for line in lines:
            if "ID" in line or "MAPA-" in line or "FOCO-" in line or "METODO-" in line or "PLANO-" in line or "KBF-" in line:
                return line.strip()

        return f"Completed: {gem_id}"

    def _ensure_gem_history(self, gem_id: str, gem_info: Dict[str, str]) -> None:
        """Garante que o histórico do GEM esteja inicializado."""
        
        if gem_id in self.gem_histories:
            return

        # Tenta carregar o histórico salvo do GEM, se existir
        saved_conversations = self.orchestrator.state.get("gem_conversations", {})
        if gem_id in saved_conversations and saved_conversations[gem_id]:
            # Usa o histórico salvo do GEM
            self.gem_histories[gem_id] = saved_conversations[gem_id].copy()
        else:
            # Inicializa novo histórico
            self.gem_histories[gem_id] = []
            shared_context = self.orchestrator.get_shared_context()

            system_message = f"""Você é o {gem_info['name']} ({gem_info['emoji']}).

{gem_info['instructions']}

{shared_context}

IMPORTANTE:
- Você faz parte de uma jornada com outros GEMs especializados
- Use as informações dos GEMs anteriores para personalizar sua abordagem
- Não peça informações que já foram coletadas anteriormente
- Use linguagem humana, calorosa e empática
- Siga rigorosamente o protocolo descrito nas suas instruções

Comece se apresentando e iniciando o protocolo."""

            self.gem_histories[gem_id].append({
                "role": "system",
                "content": system_message
            })

    def _append_user_message(
        self,
        gem_id: str,
        user_message: str,
        gem_info: Dict[str, str],
        force_completion: bool
    ) -> None:
        """Adiciona mensagem do usuário e instruções extras quando necessário."""

        self.gem_histories[gem_id].append({
            "role": "user",
            "content": user_message
        })

        if force_completion:
            self.gem_histories[gem_id].append({
                "role": "system",
                "content": self._build_force_completion_prompt(gem_info)
            })

    def _append_assistant_response(self, gem_id: str, answer: str) -> None:
        """Adiciona a resposta do LLM ao histórico."""

        self.gem_histories[gem_id].append({
            "role": "assistant",
            "content": answer
        })

    def _should_force_output_generation(self, gem_id: str, answer: str) -> bool:
        """
        Detecta se o GEM está tentando finalizar mas não gerou o output estruturado.

        Args:
            gem_id: ID do GEM
            answer: Resposta atual do GEM

        Returns:
            True se deve forçar a geração do output
        """
        if gem_id != "gem1_mestre_mapeamento":
            return False

        answer_lower = answer.lower()

        # Sinais de que completou as etapas mas não gerou output
        completion_attempt_signals = [
            "você está pronto para avançar",
            "pronto para avançar com a próxima etapa",
            "está pronto para continuar",
            "podemos avançar"
        ]

        has_signal = any(signal in answer_lower for signal in completion_attempt_signals)
        has_output_id = "MAPA-" in answer

        # Se tem sinal de conclusão mas NÃO tem o ID, precisa forçar
        return has_signal and not has_output_id

    def _finalize_interaction(
        self,
        gem_id: str,
        answer: str,
        gem_info: Dict[str, str],
        force_completion: bool
    ) -> Tuple[str, bool]:
        """Verifica e finaliza um GEM quando necessário."""

        # Verifica se precisa forçar geração do output estruturado
        if self._should_force_output_generation(gem_id, answer):
            # Injeta prompt forçando output e regenera resposta
            self.gem_histories[gem_id].append({
                "role": "system",
                "content": """ATENÇÃO: Você completou as etapas do protocolo mas não gerou o OUTPUT ESTRUTURADO OBRIGATÓRIO.

Gere AGORA o formato completo conforme as instruções, incluindo:
- ════════════════════════════════════════════
- **MAPEAMENTO M.A.P.A. COMPLETO**
- Todos os papéis identificados
- Papel prioritário com análise F.A.S.I.L.
- Matriz de priorização com scores
- Oportunidades de amplificação
- 📋 **ID DO MAPEAMENTO**: MAPA-2025-10-001
- ════════════════════════════════════════════

Gere este output AGORA e ENCERRE."""
            })

            # Regenera resposta com o prompt de força
            messages = self.gem_histories[gem_id]
            response = self.llm.invoke(messages)
            answer = getattr(response, "content", str(response)).strip()

            # Atualiza histórico com a nova resposta
            self.gem_histories[gem_id].append({
                "role": "assistant",
                "content": answer
            })

        should_finalize = force_completion or self._is_gem_complete(answer, gem_id)

        if not should_finalize:
            return answer, False

        output = self._extract_gem_output(answer, gem_id)

        # Completa o GEM e obtém mensagem de conclusão
        completion_msg, _ = self.orchestrator.complete_gem(
            gem_id,
            output
        )

        # Atualiza última resposta com eventual mensagem final
        final_answer = f"{answer}\n\n{completion_msg}".strip()

        if self.gem_histories.get(gem_id) and self.gem_histories[gem_id][-1]["role"] == "assistant":
            self.gem_histories[gem_id][-1]["content"] = final_answer

        self.orchestrator.save_gem_conversation(gem_id, self.gem_histories[gem_id])

        if gem_id in self.gem_histories:
            del self.gem_histories[gem_id]
        return final_answer, True

    def _build_force_completion_prompt(self, gem_info: Dict[str, str]) -> str:
        """Instrui o LLM a fornecer o output final estruturado."""

        return (
            "O usuário solicitou explicitamente concluir esta etapa agora. "
            "Forneça imediatamente o output final estruturado exigido para este GEM, "
            "incluindo o identificador no formato correto e uma síntese dos principais pontos. "
            f"Você é o {gem_info['name']} e deve seguir suas instruções formais."
        )

    def _is_force_completion_command(self, user_message: str) -> bool:
        """Verifica se o usuário disparou o comando de finalização manual."""

        if not user_message:
            return False

        command = user_message.strip().lower()
        return command in self._force_completion_commands

    def _stream_gem_interaction(
        self,
        gem_id: str,
        user_message: str
    ) -> Generator[Dict[str, Any], None, None]:
        """Realiza interação com streaming com um GEM."""

        gem_info = get_gem_info(gem_id)
        force_completion = self._is_force_completion_command(user_message)

        self._ensure_gem_history(gem_id, gem_info)
        self._append_user_message(gem_id, user_message, gem_info, force_completion)

        messages = self.gem_histories[gem_id]

        if not hasattr(self.llm, "stream"):
            response = self.llm.invoke(messages)
            answer = getattr(response, "content", str(response)).strip()
            self._append_assistant_response(gem_id, answer)
            final_answer, _ = self._finalize_interaction(gem_id, answer, gem_info, force_completion)
            yield {
                "type": "chunk",
                "content": final_answer,
                "accumulated": final_answer,
                "gem_id": gem_id,
                "gem_name": gem_info['name'],
                "is_orchestrator": False,
            }
            yield {
                "type": "done",
                "message": user_message,
                "answer": final_answer,
                "gem_id": gem_id,
                "gem_name": gem_info['name'],
                "is_orchestrator": False,
                "error": None,
            }
            return

        accumulated = ""

        try:
            for chunk in self.llm.stream(messages):
                text = self._extract_chunk_content(chunk)
                if not text:
                    continue

                accumulated += text

                yield {
                    "type": "chunk",
                    "content": text,
                    "accumulated": accumulated,
                    "gem_id": gem_id,
                    "gem_name": gem_info['name'],
                    "is_orchestrator": False,
                }
        except Exception as stream_error:
            # Handle errors that occur during streaming
            # If we have accumulated content, send it as a chunk before the error
            if accumulated:
                yield {
                    "type": "chunk",
                    "content": accumulated,
                    "accumulated": accumulated,
                    "gem_id": gem_id,
                    "gem_name": gem_info['name'],
                    "is_orchestrator": False,
                }
            
            # Send error event
            yield {
                "type": "error",
                "error": f"Erro durante o streaming: {str(stream_error)}",
            }
            return

        answer = accumulated.strip()

        if answer:
            self._append_assistant_response(gem_id, answer)
        else:
            self._append_assistant_response(gem_id, "")

        final_answer, _ = self._finalize_interaction(gem_id, answer, gem_info, force_completion)

        yield {
            "type": "done",
            "message": user_message,
            "answer": final_answer,
            "gem_id": gem_id,
            "gem_name": gem_info['name'],
            "is_orchestrator": False,
            "error": None,
        }

    def _extract_chunk_content(self, chunk: Any) -> str:
        """Extrai texto de um chunk retornado pelo modelo."""

        if chunk is None:
            return ""

        if hasattr(chunk, "content") and chunk.content:
            return str(chunk.content)

        if hasattr(chunk, "message") and getattr(chunk.message, "content", None):
            return str(chunk.message.content)

        if isinstance(chunk, str):
            return chunk

        return ""

    def get_welcome_message(self) -> str:
        """Retorna mensagem de boas-vindas."""
        return self.orchestrator.get_welcome_message()

    def get_status(self) -> str:
        """Retorna status da jornada."""
        return self.orchestrator.get_current_status()

    def activate_gem(self, gem_id: str) -> str:
        """Ativa um GEM específico."""
        # Limpa o histórico do GEM atual da memória, se houver e for diferente do novo GEM
        current_gem = self.orchestrator.get_current_gem()
        if current_gem and current_gem != gem_id and current_gem in self.gem_histories:
            del self.gem_histories[current_gem]
        
        # Ativa o novo GEM
        return self.orchestrator.activate_gem(gem_id)

    def reset(self) -> str:
        """Reinicia a jornada."""
        # Limpa históricos
        self.gem_histories = {}
        return self.orchestrator.reset_journey()
