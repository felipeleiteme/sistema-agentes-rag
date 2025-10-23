#!/usr/bin/env python3
"""Script para criar índice FAISS a partir da base de conhecimento"""
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from custom_embeddings import SimpleEmbeddings


def create_knowledge_base():
    """Cria e salva o índice FAISS da base de conhecimento"""
    print("Iniciando ingestão da base de conhecimento (usando embeddings TF-IDF)...")

    # Resolver caminho do arquivo de conhecimento
    base_dir = Path(__file__).resolve().parent
    knowledge_filename = "politica_rh.txt"
    candidate_paths = [
        base_dir / knowledge_filename,
        base_dir / "docs" / knowledge_filename,
        base_dir / "data" / knowledge_filename,
    ]

    knowledge_path = next((path for path in candidate_paths if path.exists()), None)

    if knowledge_path is None:
        searched_locations = "\n - ".join(str(path) for path in candidate_paths)
        raise FileNotFoundError(
            "Não foi possível localizar o arquivo de conhecimento 'politica_rh.txt'. "
            "Verifique se ele está em uma das seguintes localizações:\n - "
            + searched_locations
        )

    print(f"Carregando base de conhecimento a partir de: {knowledge_path}")

    # Carregar documento
    loader = TextLoader(str(knowledge_path), encoding="utf-8")
    documentos = loader.load()

    # Dividir em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    documentos_divididos = text_splitter.split_documents(documentos)

    for index, documento in enumerate(documentos_divididos):
        documento.metadata.setdefault("source", str(knowledge_path))
        documento.metadata["chunk_index"] = index

    print(f"Documento dividido em {len(documentos_divididos)} pedaços.")
    print("Criando banco de dados vetorial FAISS...")

    # Criar e salvar índice FAISS
    embeddings = SimpleEmbeddings()
    db = FAISS.from_documents(documentos_divididos, embeddings)
    db.save_local("faiss_index")

    print("✅ Base de conhecimento criada e salva como 'faiss_index'.")


if __name__ == "__main__":
    create_knowledge_base()
