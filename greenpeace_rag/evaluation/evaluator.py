"""
Evaluator del sistema RAG.

Implementa generación del contexto de evaluación y métricas sobre
respuestas generadas por el sistema RAG.
"""

from __future__ import annotations

from typing import Any, Dict, List

from tqdm import tqdm

from ..prompts.evaluation_prompts import (ANSWER_GENERATION_PROMPT,
                                          CORRECTNESS_EVALUATION_PROMPT,
                                          GROUNDEDNESS_EVALUATION_PROMPT,
                                          QUESTION_GENERATION_PROMPT,
                                          QUESTION_REVIEW_PROMPT,
                                          RELEVANCE_EVALUATION_PROMPT,
                                          RETRIEVAL_RELEVANCE_PROMPT)
from ..schemas.pydantic_models import (CorrectnessGrade, GeneratedAnswer,
                                       GeneratedQuestion, GroundnessCheck,
                                       GroundnessGrade, RelevanceGrade,
                                       RetrievalRelevanceGrade)
from ..utils.config import DEFAULT_PATHS
from ..utils.file_handlers import load_pickle, save_pickle


class RAGEvaluator:
    def __init__(self, greenpeace_rag: Any):
        """
        Inicializa la evaluadora con una instancia de GreenpeaceRAG.
        """
        self.rag = greenpeace_rag
        self.llm = greenpeace_rag.llm
        self.llm_model = greenpeace_rag.llm_model
        self.txt_dir = greenpeace_rag.txt_dir
        self.vector_store = None
        self.synthetic_questions: List[Dict[str, Any]] = []
        self.correctness_score = 0.0
        self.relevance_score = 0.0
        self.groundness_score = 0.0
        self.retrieval_relevance_score = 0.0

    def set_vector_store(self, vector_store: Any) -> None:
        self.vector_store = vector_store

    # ---------- Contexto de evaluación ----------
    def generate_synthetic_questions(self, amount: int = 75) -> None:
        """Genera preguntas sintéticas a partir de chunks."""
        self.synthetic_questions = []

        chunks = self.rag.generate_chunks()
        if not chunks:
            return

        # Selección simple de los primeros N (evitar dependencia en random)
        sample = chunks[: min(amount, len(chunks))]
        print(f"🔹 Generating {amount} synthetic questions...")
        for chunk in tqdm(sample):
            context = chunk.page_content
            file_name = chunk.metadata.get("file_name", "unknown")
            prompt = QUESTION_GENERATION_PROMPT.format(context=context)
            output = self.llm.with_structured_output(GeneratedQuestion).invoke([prompt])
            self.synthetic_questions.append(
                {"context": context, "question": output.question, "answer": None, "file_name": file_name}
            )
        print(f"🔹 {len(self.synthetic_questions)} synthetic questions generated")

    def generate_evaluation_answers(self) -> None:
        """Genera respuestas ground-truth para las preguntas sintéticas."""
        print(f"🔹 Generating {len(self.synthetic_questions)} evaluation answers...")
        for index, question_item in tqdm(enumerate(self.synthetic_questions)):
            question = question_item["question"]
            context = question_item["context"]
            prompt = ANSWER_GENERATION_PROMPT.format(context=context, question=question)
            output = self.llm.with_structured_output(GeneratedAnswer).invoke([prompt])
            self.synthetic_questions[index]["answer"] = output.answer
        print(f"🔹 {len(self.synthetic_questions)} evaluation answers generated")

    def questions_review(self) -> None:
        """Evalúa groundedness de las preguntas respecto al documento completo."""
        import os

        print(f"🔹 Evaluating {len(self.synthetic_questions)} questions...")
        for index, question_item in tqdm(enumerate(self.synthetic_questions)):
            file_name = question_item["file_name"]
            with open(os.path.join(self.txt_dir, file_name), "rt", encoding="utf-8") as f:
                context = f.read()
            question = question_item["question"]
            prompt = QUESTION_REVIEW_PROMPT.format(context=context, question=question)
            grade = self.llm.with_structured_output(GroundnessCheck).invoke([prompt])
            self.synthetic_questions[index]["question_review_grade"] = grade
        print(f"🔹 {len(self.synthetic_questions)} questions reviewed")
        print(f"🔹 {len(self.synthetic_questions)} questions with score >= 3")

    def dump_evaluation_context(self) -> None:
        save_pickle(self.synthetic_questions, DEFAULT_PATHS["evaluation_context_file"])
        print(f"🔹 Evaluation context dumped to {DEFAULT_PATHS['evaluation_context_file']}")

    def get_evaluation_context(self, n_questions: int | None = None) -> None:
        import os
        filepath = DEFAULT_PATHS["evaluation_context_file"]
        if not os.path.exists(filepath):
            print(f"❌ Error: No se encontró el archivo {filepath}")
            print("💡 Primero debes generar el contexto de evaluación ejecutando:")
            print("   rag_evaluator.generate_evaluation_context(amount=75)")
            print("   O selecciona la opción 1 en el script de evaluación.")
            raise FileNotFoundError(f"El archivo {filepath} no existe. Primero genera el contexto de evaluación.")
        data = load_pickle(filepath) or []
        if not data:
            print(f"⚠️  El archivo {filepath} existe pero está vacío.")
            raise ValueError(f"El archivo {filepath} está vacío. Regenera el contexto de evaluación.")
        self.synthetic_questions = data
        # mantener solo preguntas con score >= 3 si está disponible
        filtered: List[Dict[str, Any]] = []
        for q in self.synthetic_questions:
            grade = q.get("question_review_grade")
            if not grade or getattr(grade, "score", 3) >= 3:
                filtered.append(q)
        print(f"🔹 {len(filtered)} evaluation questions with score >= 3")
        # Código temporal: limitar a 2 preguntas para pruebas rápidas
        if n_questions:
            self.synthetic_questions = filtered[:n_questions]
            print(f"⚠️  Limitando a {len(self.synthetic_questions)} preguntas para pruebas")
        else:
            self.synthetic_questions = filtered
        print(f"🔹 {len(self.synthetic_questions)} evaluation questions loaded")

    # ---------- Evaluaciones ----------
    def evaluate_correctness(self) -> None:
        print(f"🔹 Evaluando {len(self.synthetic_questions)} preguntas de corrección...")
        scores: List[bool] = []
        for question_item in tqdm(self.synthetic_questions):
            question = question_item["question"]
            ground_truth_answer = question_item["answer"]
            answer = question_item.get("llm_answer", "")
            prompt = CORRECTNESS_EVALUATION_PROMPT.format(
                question=question, ground_truth_answer=ground_truth_answer, answer=answer
            )
            output = self.llm.with_structured_output(CorrectnessGrade).invoke([prompt])
            is_correct = output.is_correct
            scores.append(bool(is_correct))
        self.correctness_score = sum(scores) / len(scores) if scores else 0.0
        print(f"🔹 Correctness score: {self.correctness_score}")

    def evaluate_relevance(self) -> None:
        print(f"🔹 Evaluando {len(self.synthetic_questions)} preguntas de relevancia...")
        scores: List[bool] = []
        for question_item in tqdm(self.synthetic_questions):
            question = question_item["question"]
            answer = question_item.get("llm_answer", "")
            prompt = RELEVANCE_EVALUATION_PROMPT.format(question=question, answer=answer)
            output = self.llm.with_structured_output(RelevanceGrade).invoke([prompt])
            is_relevant = output.is_relevant
            scores.append(bool(is_relevant))
        self.relevance_score = sum(scores) / len(scores) if scores else 0.0
        print(f"🔹 Relevance score: {self.relevance_score}")

    def evaluate_groundness(self) -> None:
        print(f"🔹 Evaluando {len(self.synthetic_questions)} preguntas de groundedness...")
        scores: List[bool] = []
        for question_item in tqdm(self.synthetic_questions):
            answer = question_item.get("llm_answer", "")
            context = question_item.get("llm_answer_context", "")
            prompt = GROUNDEDNESS_EVALUATION_PROMPT.format(doc_string=context, answer=answer)
            output = self.llm.with_structured_output(GroundnessGrade).invoke([prompt])
            is_grounded = output.is_grounded
            scores.append(bool(is_grounded))
        self.groundness_score = sum(scores) / len(scores) if scores else 0.0
        print(f"🔹 Groundness score: {self.groundness_score}")

    def evaluate_retrival_relevance_grade(self) -> None:
        print(f"🔹 Evaluando {len(self.synthetic_questions)} preguntas de relevancia de recuperación...")
        scores: List[bool] = []
        for question_item in tqdm(self.synthetic_questions):
            question = question_item["question"]
            relevant_documents = question_item.get("llm_answer_docs_with_scores", [])
            doc_string = "\n\n".join([doc.page_content for doc, _ in relevant_documents]) if relevant_documents else ""
            prompt = RETRIEVAL_RELEVANCE_PROMPT.format(doc_string=doc_string, question=question)
            output = self.llm.with_structured_output(RetrievalRelevanceGrade).invoke([prompt])
            is_relevant = output.is_relevant
            scores.append(bool(is_relevant))
        self.retrieval_relevance_score = sum(scores) / len(scores) if scores else 0.0
        print(f"🔹 Retrieval relevance score: {self.retrieval_relevance_score}")

    # ---------- Pipeline de evaluación ----------
    def generate_llm_answers(self, similarity_score: int = 3) -> None:
        print(f"🔹 Generating {len(self.synthetic_questions)} LLM answers...")
        for index, question_item in tqdm(enumerate(self.synthetic_questions)):
            question = question_item["question"]
            answer, context, docs_with_scores = self.rag.generate_answers(question, similarity_score)
            self.synthetic_questions[index]["llm_answer"] = answer
            self.synthetic_questions[index]["llm_answer_context"] = context
            self.synthetic_questions[index]["llm_answer_docs_with_scores"] = docs_with_scores

    def generate_evaluation_context(self, amount: int = 75) -> None:
        self.generate_synthetic_questions(amount)
        self.generate_evaluation_answers()
        self.questions_review()
        self.dump_evaluation_context()

    def evaluate_model(self) -> None:
        self.get_evaluation_context(n_questions=None)
        # Usar el vector_store existente si ya está creado
        if not self.rag.vector_store:
            self.rag.generate_vector_store()
        self.vector_store = self.rag.vector_store
        self.generate_llm_answers(similarity_score=10)
        self.evaluate_correctness()
        self.evaluate_relevance()
        self.evaluate_groundness()
        self.evaluate_retrival_relevance_grade()
