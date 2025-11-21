"""
Gestión de modelos de embeddings para Greenpeace RAG.
"""

from typing import Any


class EmbeddingManager:
    """Factory/Manager para instanciar funciones y modelos de embeddings."""

    @staticmethod
    def embedding_function(model_name: str) -> Any:
        """Devuelve la función de embeddings compatible con LangChain-Chroma."""
        from langchain_community.embeddings import \
            SentenceTransformerEmbeddings

        return SentenceTransformerEmbeddings(model_name=model_name)

    @staticmethod
    def sentence_transformer(model_name: str):
        """Devuelve una instancia de SentenceTransformer para encode manual."""
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer(model_name)


