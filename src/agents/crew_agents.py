"""
Definição dos agentes e tarefas usando CrewAI.
Este módulo configura os agentes que usarão o LiteLLM Proxy para acessar múltiplos LLMs.
"""

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

from ..utils.config import Config
from ..tools.rag_tool import create_rag_tool


def get_llm(model_name: str = "gpt-4o", temperature: float = 0.7):
    """
    Cria uma instância de LLM usando o proxy LiteLLM.

    Args:
        model_name: Nome do modelo (gpt-4o, claude-haiku, claude-sonnet)
        temperature: Temperatura para geração de texto

    Returns:
        Instância de ChatOpenAI configurada para usar o proxy
    """
    return ChatOpenAI(
        model=model_name,
        openai_api_base=Config.LITELLM_PROXY_URL,
        openai_api_key="dummy-key",  # LiteLLM usa as chaves do config.yaml
        temperature=temperature
    )


class ResearchCrew:
    """
    Crew de pesquisa com múltiplos agentes especializados.
    """

    def __init__(self):
        """Inicializa a crew e suas ferramentas."""
        self.rag_tool = create_rag_tool()

    def create_researcher_agent(self) -> Agent:
        """
        Cria o agente pesquisador usando GPT-4o.
        """
        return Agent(
            role="Pesquisador Sênior",
            goal="Realizar pesquisas detalhadas e encontrar informações relevantes",
            backstory=(
                "Você é um pesquisador experiente com habilidade excepcional "
                "para encontrar e analisar informações. Você usa ferramentas "
                "de busca avançadas para fornecer dados precisos e contextualizados."
            ),
            llm=get_llm("gpt-4o", temperature=0.5),
            tools=[self.rag_tool],
            verbose=True,
            allow_delegation=True
        )

    def create_analyst_agent(self) -> Agent:
        """
        Cria o agente analista usando Claude Haiku (mais rápido e econômico).
        """
        return Agent(
            role="Analista de Dados",
            goal="Analisar informações e extrair insights valiosos",
            backstory=(
                "Você é um analista experiente que transforma dados brutos "
                "em insights acionáveis. Você identifica padrões, tendências "
                "e correlações importantes nos dados fornecidos."
            ),
            llm=get_llm("claude-haiku", temperature=0.3),
            verbose=True,
            allow_delegation=False
        )

    def create_writer_agent(self) -> Agent:
        """
        Cria o agente escritor usando Claude Sonnet (melhor para texto criativo).
        """
        return Agent(
            role="Redator Técnico",
            goal="Criar documentos claros, concisos e bem estruturados",
            backstory=(
                "Você é um redator técnico especializado em transformar "
                "informações complexas em documentos claros e acessíveis. "
                "Você mantém um tom profissional e organiza o conteúdo de forma lógica."
            ),
            llm=get_llm("claude-sonnet", temperature=0.7),
            verbose=True,
            allow_delegation=False
        )

    def create_research_task(self, agent: Agent, topic: str) -> Task:
        """
        Cria uma tarefa de pesquisa.
        """
        return Task(
            description=(
                f"Pesquise informações detalhadas sobre: {topic}\n"
                "Use a ferramenta RAG para buscar documentos relevantes. "
                "Compile todas as informações encontradas de forma organizada."
            ),
            expected_output=(
                "Um relatório de pesquisa contendo todas as informações "
                "relevantes encontradas, com referências às fontes."
            ),
            agent=agent
        )

    def create_analysis_task(self, agent: Agent) -> Task:
        """
        Cria uma tarefa de análise.
        """
        return Task(
            description=(
                "Analise as informações fornecidas pela pesquisa. "
                "Identifique os pontos principais, padrões e insights relevantes. "
                "Organize os dados de forma estruturada."
            ),
            expected_output=(
                "Uma análise detalhada com insights principais, "
                "conclusões e recomendações baseadas nos dados."
            ),
            agent=agent
        )

    def create_writing_task(self, agent: Agent) -> Task:
        """
        Cria uma tarefa de redação.
        """
        return Task(
            description=(
                "Com base na pesquisa e análise fornecidas, crie um documento "
                "final bem estruturado e profissional. O documento deve ser "
                "claro, objetivo e fácil de entender."
            ),
            expected_output=(
                "Um documento final completo, bem formatado e revisado, "
                "pronto para ser compartilhado."
            ),
            agent=agent
        )

    def create_crew(self, topic: str) -> Crew:
        """
        Cria e configura a crew completa.

        Args:
            topic: Tópico a ser pesquisado

        Returns:
            Crew configurada e pronta para execução
        """
        # Criar agentes
        researcher = self.create_researcher_agent()
        analyst = self.create_analyst_agent()
        writer = self.create_writer_agent()

        # Criar tarefas
        research_task = self.create_research_task(researcher, topic)
        analysis_task = self.create_analysis_task(analyst)
        writing_task = self.create_writing_task(writer)

        # Criar crew
        return Crew(
            agents=[researcher, analyst, writer],
            tasks=[research_task, analysis_task, writing_task],
            process=Process.sequential,
            verbose=True
        )


def create_simple_agent(
    role: str,
    goal: str,
    backstory: str,
    model: str = "gpt-4o",
    tools: list = None
) -> Agent:
    """
    Factory function para criar agentes personalizados rapidamente.

    Args:
        role: Papel do agente
        goal: Objetivo do agente
        backstory: História/contexto do agente
        model: Modelo LLM a usar
        tools: Lista de ferramentas (opcional)

    Returns:
        Agente configurado
    """
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=get_llm(model),
        tools=tools or [],
        verbose=True
    )
