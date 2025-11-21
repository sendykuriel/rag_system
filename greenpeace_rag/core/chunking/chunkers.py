"""
Estrategias de chunking para documentos de Greenpeace.

Este módulo contiene diferentes estrategias de fragmentación de documentos
para optimizar la recuperación de información en el sistema RAG.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import (CharacterTextSplitter,
                                      RecursiveCharacterTextSplitter)


class BaseChunker(ABC):
    """Clase base abstracta para todos los chunkers."""

    def __init__(self, chunk_params: Dict[str, Any]):
        """
        Inicializa el chunker con parámetros específicos.

        Args:
            chunk_params: Parámetros de configuración para el chunking
        """
        self.chunk_params = chunk_params

    @abstractmethod
    def chunk_files(self, txt_files: List[Path]) -> List[Any]:
        """
        Fragmenta archivos de texto en chunks.

        Args:
            txt_files: Lista de archivos de texto a procesar

        Returns:
            Lista de chunks generados
        """
        pass


class CharacterChunker(BaseChunker):
    """Chunker que divide texto por caracteres."""

    def chunk_files(self, txt_files: List[Path]) -> List[Any]:
        """Fragmenta archivos usando división por caracteres."""
        text_splitter = CharacterTextSplitter(
            separator="",
            chunk_size=self.chunk_params['chunk_char_size'],
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
            strip_whitespace=True,
        )

        texts = []
        metadatas = []
        for file_path in txt_files:
            with open(file_path, 'rt', encoding='utf-8') as f:
                content = f.read()
                texts.append(content)
                metadatas.append({"file_name": str(file_path.name)})

        return text_splitter.create_documents(texts, metadatas=metadatas)


class RecursiveCharacterChunker(BaseChunker):
    """Chunker que divide texto recursivamente por caracteres."""

    def chunk_files(self, txt_files: List[Path]) -> List[Any]:
        """Fragmenta archivos usando división recursiva por caracteres."""
        
        try:
            chunk_size = self.chunk_params['chunk_char_size']
        except KeyError:
            chunk_size = 700
        try:
            chunk_overlap = self.chunk_params['chunk_overlap']
        except KeyError:
            chunk_overlap = 200

        print(f"Chunk size to be used: {chunk_size}")
        print(f"Chunk overlap to be used: {chunk_overlap}")

        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

        texts = []
        metadatas = []
        for file_path in txt_files:
            with open(file_path, 'rt', encoding='utf-8') as f:
                content = f.read()
                texts.append(content)
                metadatas.append({"file_name": str(file_path.name)})

        return text_splitter.create_documents(texts, metadatas=metadatas)


# class SemanticDocumentChunker(BaseChunker):
#     """Chunker que divide texto basándose en similitud semántica."""

#     def __init__(self, chunk_params: Dict[str, Any]):
#         """Inicializa el chunker semántico."""
#         super().__init__(chunk_params)
#         # Usar un modelo de embedding más ligero para chunking
#         self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#     def chunk_files(self, txt_files: List[Path]) -> List[Any]:
#         """Fragmenta archivos usando división semántica."""
#         text_splitter = SemanticChunker(
#             self.embeddings,
#             breakpoint_threshold_type=self.chunk_params['breakpoint_threshold_type'],
#             breakpoint_threshold_amount=self.chunk_params['breakpoint_threshold_amount']
#         )

#         texts = []
#         metadatas = []
#         for file_path in txt_files:
#             with open(file_path, 'rt', encoding='utf-8') as f:
#                 content = f.read()
#                 texts.append(content)
#                 metadatas.append({"file_name": str(file_path.name)})

#         return text_splitter.create_documents(texts, metadatas=metadatas)


class DocumentTypeChunker(BaseChunker):
    """Chunker que adapta la estrategia según el tipo de documento."""

    def chunk_files(self, txt_files: List[Path]) -> List[Any]:
        """
        Fragmenta archivos adaptando la estrategia según el tipo de documento.

        TODO: Implementar lógica específica por tipo de documento
        """
        # Por ahora usa chunking recursivo como fallback
        fallback_chunker = RecursiveCharacterChunker(self.chunk_params)
        return fallback_chunker.chunk_files(txt_files)


class ChunkerFactory:
    """Factory para crear chunkers según la estrategia especificada."""

    _chunkers = {
        "characters": CharacterChunker,
        "recursive_characters": RecursiveCharacterChunker,
        # "semantic": SemanticDocumentChunker,
        "documents_type": DocumentTypeChunker,
    }

    @classmethod
    def create_chunker(cls, strategy: str, chunk_params: Dict[str, Any]) -> BaseChunker:
        """
        Crea un chunker según la estrategia especificada.

        Args:
            strategy: Estrategia de chunking a usar
            chunk_params: Parámetros de configuración

        Returns:
            Instancia del chunker correspondiente

        Raises:
            ValueError: Si la estrategia no es válida
        """
        if strategy not in cls._chunkers:
            raise ValueError(f"Estrategia de chunking no válida: {strategy}")

        chunker_class = cls._chunkers[strategy]
        return chunker_class(chunk_params)

    @classmethod
    def get_available_strategies(cls) -> List[str]:
        """Retorna las estrategias de chunking disponibles."""
        return list(cls._chunkers.keys())
