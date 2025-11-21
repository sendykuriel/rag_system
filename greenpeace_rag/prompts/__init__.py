"""
Prompts module.

Contiene todos los prompts utilizados en el sistema RAG.
"""

from .evaluation_prompts import (ANSWER_GENERATION_PROMPT,
                                 CORRECTNESS_EVALUATION_PROMPT,
                                 GROUNDEDNESS_EVALUATION_PROMPT,
                                 QUESTION_GENERATION_PROMPT,
                                 QUESTION_REVIEW_PROMPT,
                                 RELEVANCE_EVALUATION_PROMPT,
                                 RETRIEVAL_RELEVANCE_PROMPT)
from .rag_prompts import (DOCUMENT_FILTER_PROMPT, RAG_SYSTEM_PROMPT,
                          get_rag_chat_prompt)

__all__ = [
    # RAG prompts
    "RAG_SYSTEM_PROMPT",
    "get_rag_chat_prompt",
    "DOCUMENT_FILTER_PROMPT",
    # Evaluation prompts
    "QUESTION_GENERATION_PROMPT",
    "ANSWER_GENERATION_PROMPT", 
    "QUESTION_REVIEW_PROMPT",
    "CORRECTNESS_EVALUATION_PROMPT",
    "RELEVANCE_EVALUATION_PROMPT",
    "GROUNDEDNESS_EVALUATION_PROMPT",
    "RETRIEVAL_RELEVANCE_PROMPT"
]
