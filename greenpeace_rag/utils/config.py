"""
Configuración y constantes del sistema Greenpeace RAG.

Contiene configuraciones por defecto y constantes utilizadas en todo el sistema.
"""

from pathlib import Path
from typing import Any, Dict

# Configuración por defecto
DEFAULT_CONFIG = {
    "llm_provider": "ollama",
    "llm_model": "llama3.1:8b",
    "txt_dir": "/Users/urielsendyk/Documents/itba/13 LLMs/docs_load_txt",
    "chroma_db_path": "./chroma_db",
    "collection_name": "greenpeace_docs",
    "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "chunk_strategy": "paragraph",
    "chunk_params": {
        "chunk_char_size": 700,
        "chunk_overlap": 200
    }
}

# Estrategias de chunking disponibles
CHUNKING_STRATEGIES = [
    "characters",
    "recursive_characters",
    "documents_type",
    "semantic"
]

# Modelos de embedding recomendados
RECOMMENDED_EMBEDDING_MODELS = [
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "sentence-transformers/all-MiniLM-L6-v2",
    "sentence-transformers/all-mpnet-base-v2"
]

# Configuración de LLM por defecto
DEFAULT_LLM_CONFIG = {
    "temperature": 0.7,
    "num_ctx": 4096
}

# Configuración de evaluación
EVALUATION_CONFIG = {
    "default_question_amount": 75,
    "similarity_score_threshold": 3,
    "groundness_threshold": 3
}

# Rutas de archivos
# Usar ruta absoluta basada en el directorio del proyecto
_PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_PATHS = {
    "evaluation_context_file": str(_PROJECT_ROOT / "evaluation_context.pkl"),
    "evaluation_context_json": str(_PROJECT_ROOT / "evaluation_context.json")
}


def get_default_config() -> Dict[str, Any]:
    """Obtiene la configuración por defecto del sistema."""
    return DEFAULT_CONFIG.copy()


def validate_chunking_strategy(strategy: str) -> bool:
    """Valida si una estrategia de chunking es válida."""
    return strategy in CHUNKING_STRATEGIES


def validate_embedding_model(model: str) -> bool:
    """Valida si un modelo de embedding es recomendado."""
    return model in RECOMMENDED_EMBEDDING_MODELS


def get_chunking_params(strategy: str) -> Dict[str, Any]:
    """Obtiene parámetros por defecto para una estrategia de chunking."""
    params = DEFAULT_CONFIG["chunk_params"].copy()

    if strategy == "characters":
        params.update({
            "chunk_char_size": 1500,
            "chunk_overlap": 20
        })
    elif strategy == "recursive_characters":
        params.update({
            "chunk_char_size": 500,
            "chunk_overlap": 100
        })
    elif strategy == "semantic":
        params.update({
            "breakpoint_threshold_type": "percentile",
            "breakpoint_threshold_amount": 95
        })

    return params
