"""
Métricas de evaluación para el sistema RAG.
"""

from typing import Iterable


class CorrectnessMetric:
    @staticmethod
    def score(values: Iterable[bool]) -> float:
        values = list(values)
        return sum(1 for v in values if bool(v)) / len(values) if values else 0.0


class RelevanceMetric:
    @staticmethod
    def score(values: Iterable[bool]) -> float:
        values = list(values)
        return sum(1 for v in values if bool(v)) / len(values) if values else 0.0


class GroundnessMetric:
    @staticmethod
    def score(values: Iterable[bool]) -> float:
        values = list(values)
        return sum(1 for v in values if bool(v)) / len(values) if values else 0.0


class RetrievalRelevanceMetric:
    @staticmethod
    def score(values: Iterable[bool]) -> float:
        values = list(values)
        return sum(1 for v in values if bool(v)) / len(values) if values else 0.0