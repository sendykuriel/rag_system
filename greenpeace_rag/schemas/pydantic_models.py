"""
Modelos Pydantic para el sistema Greenpeace RAG.

Este módulo contiene todos los modelos de datos utilizados en el sistema,
incluyendo modelos para evaluación, respuestas generadas y verificaciones.
"""

from pydantic import BaseModel, Field


class GeneratedQuestion(BaseModel):
    """Modelo para preguntas generadas sintéticamente."""
    question: str = Field(description="A generated question as a sentence")


class GeneratedAnswer(BaseModel):
    """Modelo para respuestas generadas."""
    answer: str = Field(description="A generated answer as a sentence")


class GroundnessCheck(BaseModel):
    """Modelo para verificación de groundedness (base en documentos)."""
    explanation: str = Field(description="Explain your reasoning for the score")
    score: int = Field(description="Your evaluation and reasoning for the rating, from 1 to 5.", gt=0, lt=6)


class CorrectnessGrade(BaseModel):
    """Modelo para evaluación de corrección de respuestas."""
    explanation: str = Field(description="Explain your reasoning for the score")
    is_correct: bool = Field(description="True if the answer is correct, False otherwise.")


class RelevanceGrade(BaseModel):
    """Modelo para evaluación de relevancia de respuestas."""
    explanation: str = Field(description="Explain your reasoning for the score")
    is_relevant: bool = Field(description="True if the answer addresses the question, False otherwise")


class GroundnessGrade(BaseModel):
    """Modelo para evaluación de groundedness de respuestas."""
    explanation: str = Field(description="Explain your reasoning for the score")
    is_grounded: bool = Field(description="True if the answer is not grounded on the documents, False otherwise")


class RetrievalRelevanceGrade(BaseModel):
    """Modelo para evaluación de relevancia de documentos recuperados."""
    explanation: str = Field(description="Explain your reasoning for the score.")
    is_relevant: bool = Field(description="True if the retrieved documents are relevant to the question, False otherwise.")


class RankingQuestions(BaseModel):
    'Modelo para preguntas de ranking.'
    questions: set[str] = Field(description="Created questions with a question mark '?' at the end")