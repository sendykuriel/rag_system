"""
Utils module.

Contiene utilidades compartidas y configuraciones.
"""

from .config import (CHUNKING_STRATEGIES, DEFAULT_CONFIG, DEFAULT_LLM_CONFIG,
                     EVALUATION_CONFIG, RECOMMENDED_EMBEDDING_MODELS,
                     get_chunking_params, get_default_config,
                     validate_chunking_strategy, validate_embedding_model)
from .file_handlers import (ensure_directory_exists, get_file_info, load_json,
                            load_pickle, read_text_files, save_json,
                            save_pickle)

__all__ = [
    # Config
    "DEFAULT_CONFIG",
    "CHUNKING_STRATEGIES", 
    "RECOMMENDED_EMBEDDING_MODELS",
    "DEFAULT_LLM_CONFIG",
    "EVALUATION_CONFIG",
    "get_default_config",
    "validate_chunking_strategy",
    "validate_embedding_model",
    "get_chunking_params",
    # File handlers
    "read_text_files",
    "save_pickle",
    "load_pickle", 
    "save_json",
    "load_json",
    "ensure_directory_exists",
    "get_file_info"
]
