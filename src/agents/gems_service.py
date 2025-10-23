"""
Serviço principal do Sistema SAC Learning GEMS.
Integra o orquestrador com os agentes GEM especializados.
"""

from dataclasses import dataclass
from typing import Optional
from langchain_ollama import ChatOllama

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
        self.llm = llm or ChatOllama(
            model="llama3.2:3b",
            temperature=0.4,  # Mais determinístico = mais rápido
            num_predict=350,  # Respostas concisas e rápidas
            num_ctx=1536,  # Contexto reduzido para processar mais rápido
            request_timeout=25.0,  # Timeout reduzido
            num_thread=4,  # Otimiza uso de CPU
        )

        self.orchestrator = GEMOrchestrator(state_file=state_file)

        # Histórico de mensagens por GEM durante a sessão
        self.gem_histories = {}

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

        # Inicializa histórico do GEM se necessário
        if gem_id not in self.gem_histories:
            self.gem_histories[gem_id] = []

            # Obtém contexto compartilhado dos GEMs anteriores
            shared_context = self.orchestrator.get_shared_context()

            # Primeira interação: adiciona as instruções do GEM com contexto
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

        # Adiciona mensagem do usuário ao histórico
        self.gem_histories[gem_id].append({
            "role": "user",
            "content": user_message
        })

        # Gera resposta usando o LLM com histórico completo
        try:
            # Constrói o prompt com histórico
            messages = self.gem_histories[gem_id]

            # Invoca o LLM
            response = self.llm.invoke(messages)
            answer = getattr(response, "content", str(response))

            # Adiciona resposta ao histórico
            self.gem_histories[gem_id].append({
                "role": "assistant",
                "content": answer
            })

            # Detecta se o GEM finalizou e gerou um ID/output estruturado
            if self._is_gem_complete(answer, gem_id):
                # Extrai o output estruturado
                output = self._extract_gem_output(answer, gem_id)

                # Salva histórico de conversas do GEM
                self.orchestrator.save_gem_conversation(
                    gem_id,
                    self.gem_histories[gem_id]
                )

                # Atualiza contexto compartilhado
                self.orchestrator.update_shared_context(gem_id, output)

                # Marca como completo no orquestrador
                completion_msg, next_gem = self.orchestrator.complete_gem(
                    gem_id,
                    output
                )

                # Limpa histórico do GEM completado da sessão
                if gem_id in self.gem_histories:
                    del self.gem_histories[gem_id]

                # Adiciona mensagem de conclusão à resposta
                answer += f"\n\n{completion_msg}"

            return GEMResponse(
                answer=answer.strip(),
                gem_id=gem_id,
                gem_name=gem_info['name']
            )

        except Exception as e:
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
        # Padrões de IDs gerados pelos GEMs
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
        return pattern and pattern in response

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

    def get_welcome_message(self) -> str:
        """Retorna mensagem de boas-vindas."""
        return self.orchestrator.get_welcome_message()

    def get_status(self) -> str:
        """Retorna status da jornada."""
        return self.orchestrator.get_current_status()

    def reset(self) -> str:
        """Reinicia a jornada."""
        # Limpa históricos
        self.gem_histories = {}
        return self.orchestrator.reset_journey()
