"""Ferramenta RAG para busca na base de conhecimento de RH"""
from crewai.tools import BaseTool
from langchain_community.vectorstores import FAISS
from custom_embeddings import SimpleEmbeddings


class BuscaConhecimentoRHTool(BaseTool):
    """Ferramenta para buscar informações na base de conhecimento de RH"""

    name: str = "Ferramenta de Busca na Base de Conhecimento de RH"
    description: str = (
        "Usa esta ferramenta para responder perguntas sobre as políticas de RH da empresa, "
        "como férias, bônus e regime de contratação."
    )

    def _run(self, pergunta: str) -> str:
        """Executa a busca na base de conhecimento"""
        embeddings = SimpleEmbeddings()
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

        print(f"--- Ferramenta RAG Recebeu a Pergunta: {pergunta}")
        documentos = retriever.invoke(pergunta)

        if not documentos:
            print("--- Nenhum contexto relevante encontrado. Retornando mensagem padrão.")
            return ""

        documentos_ordenados = sorted(
            documentos, key=lambda doc: doc.metadata.get("chunk_index", float("inf"))
        )

        trechos_unicos = []
        vistos = set()

        for doc in documentos_ordenados:
            trecho = doc.page_content.strip()
            if trecho and trecho not in vistos:
                trechos_unicos.append(trecho)
                vistos.add(trecho)

        contexto = "\n\n---\n\n".join(trechos_unicos)
        print(f"--- Contexto Encontrado: {contexto[:200]}...")
        return contexto


buscar_conhecimento_rh = BuscaConhecimentoRHTool()
