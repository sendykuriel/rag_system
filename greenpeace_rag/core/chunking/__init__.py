"""
Chunking strategies module.

Contiene diferentes estrategias para fragmentar documentos de texto.
"""

from .chunkers import (BaseChunker, CharacterChunker, ChunkerFactory,
                       DocumentTypeChunker, RecursiveCharacterChunker)

__all__ = [
    "BaseChunker",
    "CharacterChunker", 
    "RecursiveCharacterChunker",
    "SemanticDocumentChunker",
    "ChunkerFactory"
]
