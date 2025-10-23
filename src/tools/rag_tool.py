"""
Ferramenta RAG usando LangChain e FAISS.
Permite buscar informações em documentos indexados.
"""

from pathlib import Path
from typing import List, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from crewai_tools import BaseTool

from ..utils.config import Config


class RAGTool(BaseTool):
    name: str = "RAG Search Tool"
    description: str = (
        "Ferramenta para buscar informações relevantes em documentos. "
        "Use esta ferramenta quando precisar encontrar informações específicas "
        "em documentos previamente indexados. Passe sua consulta como texto."
    )

    def __init__(self, docs_path: Optional[Path] = None):
        """
        Inicializa a ferramenta RAG.

        Args:
            docs_path: Caminho para os documentos (padrão: Config.DOCS_DIR)
        """
        super().__init__()
        self.docs_path = docs_path or Config.DOCS_DIR
        self.vectorstore_path = Config.DATA_DIR / "vectorstore"
        self.vectorstore = None
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)

    def _load_documents(self) -> List:
        """Carrega documentos do diretório especificado."""
        loader = DirectoryLoader(
            str(self.docs_path),
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=True
        )
        documents = loader.load()

        # Dividir documentos em chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)

        return chunks

    def create_vectorstore(self) -> None:
        """Cria e salva o vectorstore a partir dos documentos."""
        print("📚 Carregando documentos...")
        chunks = self._load_documents()

        if not chunks:
            print("⚠️  Nenhum documento encontrado!")
            return

        print(f"📄 {len(chunks)} chunks criados")
        print("🔄 Criando vectorstore...")

        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.vectorstore.save_local(str(self.vectorstore_path))

        print(f"✅ Vectorstore salvo em: {self.vectorstore_path}")

    def load_vectorstore(self) -> None:
        """Carrega o vectorstore existente."""
        if not self.vectorstore_path.exists():
            print("⚠️  Vectorstore não encontrado. Criando novo...")
            self.create_vectorstore()
            return

        self.vectorstore = FAISS.load_local(
            str(self.vectorstore_path),
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print("✅ Vectorstore carregado")

    def _run(self, query: str, k: int = 3) -> str:
        """
        Executa a busca RAG.

        Args:
            query: Consulta de busca
            k: Número de resultados a retornar

        Returns:
            String com os resultados encontrados
        """
        if not self.vectorstore:
            self.load_vectorstore()

        if not self.vectorstore:
            return "Erro: Vectorstore não disponível"

        # Buscar documentos relevantes
        results = self.vectorstore.similarity_search(query, k=k)

        if not results:
            return "Nenhum resultado encontrado para a consulta."

        # Formatar resultados
        formatted_results = []
        for i, doc in enumerate(results, 1):
            formatted_results.append(
                f"[Resultado {i}]\n"
                f"Fonte: {doc.metadata.get('source', 'Desconhecida')}\n"
                f"Conteúdo: {doc.page_content}\n"
            )

        return "\n".join(formatted_results)


def create_rag_tool(docs_path: Optional[Path] = None) -> RAGTool:
    """
    Factory function para criar uma instância da RAGTool.

    Args:
        docs_path: Caminho opcional para os documentos

    Returns:
        Instância configurada da RAGTool
    """
    tool = RAGTool(docs_path=docs_path)
    tool.load_vectorstore()
    return tool
