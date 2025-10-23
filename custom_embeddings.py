"""Embeddings customizados usando TF-IDF (sem PyTorch)"""
from typing import List
from langchain_core.embeddings import Embeddings
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class SimpleEmbeddings(Embeddings):
    """Embeddings baseados em TF-IDF para evitar dependência do PyTorch"""

    def __init__(self, max_features: int = 384):
        """
        Args:
            max_features: Dimensão dos vetores de embedding
        """
        self.vectorizer = TfidfVectorizer(max_features=max_features)
        self.fitted = False
        self.dim = max_features

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Cria embeddings para uma lista de documentos"""
        if not self.fitted:
            self.vectorizer.fit(texts)
            self.fitted = True

        vectors = self.vectorizer.transform(texts).toarray()
        return self._normalize_vectors(vectors)

    def embed_query(self, text: str) -> List[float]:
        """Cria embedding para uma query única"""
        if not self.fitted:
            self.vectorizer.fit([text])
            self.fitted = True

        vector = self.vectorizer.transform([text]).toarray()[0]
        return self._normalize_vectors([vector])[0]

    def _normalize_vectors(self, vectors: np.ndarray) -> List[List[float]]:
        """Normaliza vetores para dimensão fixa"""
        embeddings = []
        for vec in vectors:
            if len(vec) < self.dim:
                padded = np.pad(vec, (0, self.dim - len(vec)), mode='constant')
                embeddings.append(padded.tolist())
            else:
                embeddings.append(vec[:self.dim].tolist())
        return embeddings
