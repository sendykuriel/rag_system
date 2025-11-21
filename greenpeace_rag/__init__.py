"""
Greenpeace RAG Package

Un sistema de Retrieval-Augmented Generation (RAG) especializado en documentos de Greenpeace.
Proporciona funcionalidades para chunking, embedding, recuperación y evaluación de documentos.
"""

__version__ = "0.1.0"
__author__ = "Uriel Sendyk"

import os
# Para compatibilidad temporal, importamos desde el archivo original
import sys

# Importaciones principales del sistema RAG
from .core import GreenpeaceRAG
# Importaciones de evaluación
from .evaluation import RAGEvaluator
# Importaciones principales disponibles
from .prompts import *
from .schemas import *
from .utils import *

__all__ = [
    # Clases principales
    "GreenpeaceRAG",
    "RAGEvaluator",
    # Schemas
    "GeneratedQuestion",
    "GeneratedAnswer",
    "GroundnessCheck",
    "CorrectnessGrade",
    "RelevanceGrade",
    "GroundnessGrade",
    "RetrievalRelevanceGrade",
    # Prompts principales
    "RAG_SYSTEM_PROMPT",
    "get_rag_chat_prompt",
    "DOCUMENT_FILTER_PROMPT",
    # Utilidades
    "DEFAULT_CONFIG",
    "CHUNKING_STRATEGIES",
    "RECOMMENDED_EMBEDDING_MODELS",
    "get_default_config",
    "validate_chunking_strategy",
    "validate_embedding_model",
    "get_chunking_params",
    "read_text_files",
    "save_pickle",
    "load_pickle",
    "save_json",
    "load_json",
    "ensure_directory_exists",
    "get_file_info"
]
