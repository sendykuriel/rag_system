"""
Evaluation module.

Contiene funcionalidades para evaluar el rendimiento del sistema RAG.
"""

from .evaluator import RAGEvaluator
from .metrics.rag_metrics import (CorrectnessMetric, GroundnessMetric,
                                  RelevanceMetric, RetrievalRelevanceMetric)

__all__ = [
    "RAGEvaluator",
    "CorrectnessMetric",
    "RelevanceMetric",
    "GroundnessMetric",
    "RetrievalRelevanceMetric",
]
