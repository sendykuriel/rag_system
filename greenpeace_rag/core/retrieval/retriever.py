"""
Módulo de recuperación de documentos para el sistema RAG.

Este módulo contiene la lógica para recuperar y filtrar documentos relevantes
usando ChromaDB y LLM para evaluación de relevancia.
"""

from typing import Any, List, Optional, Tuple

from langchain_chroma import Chroma
from langchain_core.documents import Document

from greenpeace_rag.prompts.rag_prompts import (DOCUMENT_FILTER_PROMPT,
                                                KEYWORDS_PROMPT,
                                                RANKING_PROMPT)
from greenpeace_rag.schemas.pydantic_models import (RankingQuestions,
                                                    RelevanceGrade)


class DocumentRetriever:
    """
    Clase para recuperar y filtrar documentos relevantes.

    Maneja la búsqueda semántica en ChromaDB y el filtrado de documentos
    usando LLM para asegurar relevancia.
    """

    def __init__(self, vector_store: Chroma, llm: Any):
        """
        Inicializa el recuperador de documentos.

        Args:
            vector_store: Instancia de ChromaDB para búsqueda semántica
            llm: Modelo de lenguaje para filtrado de documentos
        """
        self.vector_store = vector_store
        self.llm = llm

    def get_relevant_documents(
        self,
        question: str,
        k: int = 3,
        filter_by_relevance: bool = True,
        ranking_questions: bool = False
    ) -> List[Tuple[Document, float]]:
        """
        Obtiene documentos relevantes para una pregunta.

        Args:
            question: Pregunta a responder
            k: Número de documentos a recuperar inicialmente
            filter_by_relevance: Si True, filtra documentos usando LLM

        Returns:
            Lista de tuplas (documento, score) con documentos relevantes
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado.")

        print(f'🔍 Buscando documentos relevantes (k={k})...')

        
        # Obtener keywords para la pregunta
        # keywords = self.get_keywords(question)
        keywords = None
        if keywords:
            docs_with_scores = self.vector_store.similarity_search_with_score(
                question, k=k, where_document={"$contains": keywords}
            )
        else:
            docs_with_scores = self.vector_store.similarity_search_with_score(
                question, k=k
            )
        
        
        if ranking_questions:
            print(f"🔍 Generando preguntas de ranking...")
            amount_text = "five" # cantidad de preguntas extra
            k_ranking = 2 # cantidad de docs por pregunta extra
            
            print(f"🔍 Generando preguntas de ranking...")
            ranking_questions = self.generate_ranking_questions(question, amount_text=amount_text)
            for question in ranking_questions:
                docs_with_scores.extend(self.vector_store.similarity_search_with_score(question, k=k_ranking))
            
            # Quitar duplicados usando hash del contenido del documento (Document no es hashable)
            seen = set()
            unique_docs = []
            for doc, score in docs_with_scores:
                # Usar contenido como identificador único
                doc_id = hash(doc.page_content)
                if doc_id not in seen:
                    seen.add(doc_id)
                    unique_docs.append((doc, score))
            docs_with_scores = unique_docs
            # Update the score of the document using the RRF formula: 1 / (rank + k)
            for doc, score in docs_with_scores:
                score = 1 / (score + k_ranking)
            # Ordenar por score
            docs_with_scores = sorted(docs_with_scores, key=lambda x: x[1], reverse=True)
            # Tomar los k mejores
            docs_with_scores = docs_with_scores[:k]
        
        
        # Filtrar documentos por relevancia usando LLM si está habilitado
        print(f"🔍 filter_by_relevance: {filter_by_relevance}")
        if filter_by_relevance:
            print(f"🔍 Filtrando documentos por relevancia usando LLM...")
            filtered_docs = []
            for doc, score in docs_with_scores:
                is_relevant, explanation = self.filter_documents_by_LLM_relevance(question, doc.page_content)
                if is_relevant:
                    filtered_docs.append((doc, score))
                else:
                    print(f"🚫 Documento filtrado: {doc.metadata.get('filename', 'unknown')}")
                    print(f" Score: {score}")
                    print(f" Pregunta: {question}")
                    print(f" Explicación: {explanation}")

            if not filtered_docs:
                print(f"⚠️  No se encontraron documentos relevantes para: {question}")

            return filtered_docs
        
        return docs_with_scores

    def get_keywords(self, question: str) -> List[str]:
        """
        Obtiene keywords para la pregunta.
        """
        prompt = KEYWORDS_PROMPT.format(question=question)
        output = self.llm.invoke([prompt])
        return output.keywords
    
    def filter_documents_by_LLM_relevance(self, question: str, context: str) -> Tuple[bool, str]:
        """
        Filtra documentos por relevancia usando LLM.

        Args:
            question: Pregunta original
            context: Contenido del documento a evaluar

        Returns:
            Tupla (es_relevante, explicación)
        """
        prompt = DOCUMENT_FILTER_PROMPT.format(question=question, context=context)
        output = self.llm.with_structured_output(RelevanceGrade).invoke([prompt])
        return output.is_relevant, output.explanation
    
    def generate_ranking_questions(self, question: str, amount_text: str = "5") -> List[str]:
        """
        Genera preguntas de ranking para la pregunta.
        """
        prompt = RANKING_PROMPT.format(question=question, amount=amount_text)
        output = self.llm.with_structured_output(RankingQuestions).invoke([prompt])
        return output.questions
    
    def get_top_k_documents(
        self,
        question: str,
        k: int = 3,
        score_threshold: Optional[float] = None
    ) -> List[Document]:
        """
        Obtiene los top K documentos sin filtrado por LLM.

        Args:
            question: Pregunta a responder
            k: Número de documentos a recuperar
            score_threshold: Umbral mínimo de score (opcional)

        Returns:
            Lista de documentos
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado.")

        docs_with_scores = self.vector_store.similarity_search_with_score(
            question, k=k
        )

        if score_threshold is not None:
            # Filtrar por umbral de score
            filtered = [
                doc for doc, score in docs_with_scores
                if score <= score_threshold
            ]
            return filtered

        return [doc for doc, _ in docs_with_scores]

    def get_documents_with_scores(
        self,
        question: str,
        k: int = 3
    ) -> List[Tuple[Document, float]]:
        """
        Obtiene documentos con sus scores de similitud.

        Args:
            question: Pregunta a responder
            k: Número de documentos a recuperar

        Returns:
            Lista de tuplas (documento, score)
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado.")

        return self.vector_store.similarity_search_with_score(question, k=k)
