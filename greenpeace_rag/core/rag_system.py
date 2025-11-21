from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from ..models import EmbeddingManager, LLMManager
from ..prompts.rag_prompts import get_rag_chat_prompt
from ..utils.config import get_chunking_params, validate_chunking_strategy
from .chunking import ChunkerFactory
from .retrieval import DocumentRetriever


class GreenpeaceRAG:
    def __init__(
            self,
            llm_provider: str = "ollama",
            llm_model: str = "llama3.1:8b",
            txt_dir: str = "/Users/urielsendyk/Documents/itba/13 LLMs/docs_load_txt",
            chroma_db_path: str = "./chroma_db",
            collection_name: str = "greenpeace_docs",
            embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            chunk_strategy: str = "recursive_characters",
            chunk_params: Optional[Dict] = None):

        # Configuración básica
        self.txt_dir = txt_dir
        self.chroma_db_path = chroma_db_path
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.chunk_strategy = chunk_strategy
        self.llm_provider = llm_provider
        self.llm_model = llm_model

        # Configurar parámetros de chunking
        if chunk_params is None:
            self.chunk_params = get_chunking_params(chunk_strategy)
        else:
            self.chunk_params = chunk_params

        # Validar estrategia de chunking
        if not validate_chunking_strategy(chunk_strategy):
            raise ValueError(f"Estrategia de chunking no válida: {chunk_strategy}")

        # Inicializar LLM mediante manager
        self.llm = LLMManager.create(
            provider=self.llm_provider,
            model=self.llm_model,
            temperature=0.7,
            num_ctx=4096,
        )

        # Atributos del sistema
        self.chunks = []
        self.embeddings = None
        self.vector_store = None
        self.rag_chain = None
        self.retriever = None  # Se inicializará después de crear el vector_store

        # Inicializar evaluadora (se importa aquí para evitar dependencias circulares)
        try:
            from ..evaluation.evaluator import RAGEvaluator
            self.evaluadora = RAGEvaluator(self)
        except ImportError:
            self.evaluadora = None
            print("⚠️  Evaluador no disponible aún. Se inicializará cuando esté migrado.")

    def generate_chunks(self) -> List[Any]:
        """
        Genera chunks desde un directorio de archivos de texto.

        Returns:
            Lista de chunks generados
        """
        txt_files = list(Path(self.txt_dir).glob("*.txt"))
        if not txt_files:
            print(f"⚠️  No se encontraron archivos TXT en {self.txt_dir}")
            return []

        print(f"📄 Procesando {len(txt_files)} archivos con estrategia: {self.chunk_strategy}")

        # Crear chunker usando el factory
        chunker = ChunkerFactory.create_chunker(self.chunk_strategy, self.chunk_params)

        # Generar chunks
        chunks = chunker.chunk_files(txt_files)

        self.chunks = chunks
        print(f"✅ Generados {len(chunks)} chunks")
        return chunks

    def generate_embeddings(self, chunks: Optional[List[Any]] = None) -> None:
        """
        Genera embeddings para una lista de chunks.

        Args:
            chunks: Lista de chunks. Si es None, usa self.chunks
        """
        if chunks is None:
            chunks = self.chunks

        if not chunks:
            print("⚠️  No hay chunks para generar embeddings")
            return

        print(f"🔢 Generando embeddings con {self.embedding_model}...")
        model = EmbeddingManager.sentence_transformer(self.embedding_model)

        texts = [chunk.page_content for chunk in chunks]
        self.embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        print(f"✅ Embeddings generados: {self.embeddings.shape}")

    def generate_vector_store(self) -> None:
        """Genera y configura el vector store."""
        print(f"🗄️  Creando vector store en {self.chroma_db_path}")

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=EmbeddingManager.embedding_function(self.embedding_model),
            persist_directory=self.chroma_db_path,
        )

        # Si la colección ya tiene datos, consultar si se desea regenerar
        try:
            existing_count = self.vector_store._collection.count()  # type: ignore[attr-defined]
        except Exception:
            existing_count = 0

        if existing_count > 0:
            answer = input(
                f"La colección '{self.collection_name}' ya tiene {existing_count} documentos. "
                "¿Desea REGENERAR el índice (recalcular chunks y reindexar)? [y/N]: "
            ).strip().lower()
            if answer in ("y", "yes", "s", "si", "sí"):
                print("🧹 Regenerando índice: eliminando colección previa...")
                try:
                    # Eliminar colección y recrearla limpia
                    self.vector_store._client.delete_collection(self.collection_name)  # type: ignore[attr-defined]
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar la colección existente: {e}. Se continuará recreando.")
                # Re-crear el vector store limpio
                self.vector_store = Chroma(
                    collection_name=self.collection_name,
                    embedding_function=EmbeddingManager.embedding_function(self.embedding_model),
                    persist_directory=self.chroma_db_path,
                )
            else:
                print("➡️  Usando índice existente. No se reindexan documentos.")
                # Inicializar el retriever incluso cuando se usa el índice existente
                self.retriever = DocumentRetriever(self.vector_store, self.llm)
                return

        # Agregar documentos (indexado inicial o tras regeneración)
        if self.chunks:
            total = len(self.chunks)
            print(f"📚 Agregando {total} chunks al vector store en lotes...")
            # Límite reportado por Chroma ~5461; usar margen de seguridad
            batch_size = 5000
            for start in range(0, total, batch_size):
                end = min(start + batch_size, total)
                batch = self.chunks[start:end]
                self.vector_store.add_documents(batch)
                print(f"   - Lote agregado: {start}-{end} ({end-start} docs)")
            print("✅ Todos los chunks fueron agregados al vector store")

        # Inicializar el retriever después de crear el vector store
        self.retriever = DocumentRetriever(self.vector_store, self.llm)

    def generate_answers(
        self,
        question: str,
        similarity_score: int = 3
    ) -> Tuple[str, str, List[Tuple[Any, float]]]:
        """
        Genera una respuesta a una pregunta usando el vector store.

        Args:
            question: Pregunta a responder
            similarity_score: Número de documentos a recuperar

        Returns:
            Tupla (respuesta, contexto, documentos_con_scores)
        """
        if not self.vector_store:
            raise ValueError("Vector store no inicializado. Ejecuta rag_setup() primero.")

        if not self.retriever:
            raise ValueError("Retriever no inicializado. Ejecuta rag_setup() primero.")

        # Obtener documentos relevantes usando el retriever
        docs_with_scores = self.retriever.get_relevant_documents(
            question, k=similarity_score, filter_by_relevance=True, ranking_questions=False
        )

        if not docs_with_scores:
            return "No tengo información suficiente en los documentos para responder eso.", "", []

        # Preparar contexto
        docs = [doc for doc, score in docs_with_scores]
        context = "\n---\n".join([doc.page_content for doc in docs])

        # Configurar prompt
        prompt = get_rag_chat_prompt()

        # Crear cadena RAG
        self.rag_chain = (
            {
                "context": RunnableLambda(lambda x: context),
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        # Generar respuesta
        response = self.rag_chain.invoke(question)

        return response, context, docs_with_scores

    def filter_documents(self, question: str, context: str) -> Tuple[bool, str]:
        """
        Filtra documentos por relevancia usando LLM.

        Args:
            question: Pregunta original
            context: Contenido del documento a evaluar

        Returns:
            Tupla (es_relevante, explicación)
        """
        if not self.retriever:
            raise ValueError("Retriever no inicializado. Ejecuta rag_setup() primero.")

        return self.retriever.filter_documents(question, context)

    def get_relevant_documents(
        self,
        question: str,
        similarity_score: int = 3
    ) -> List[Tuple[Any, float]]:
        """
        Obtiene documentos relevantes para una pregunta.

        Args:
            question: Pregunta a responder
            similarity_score: Número de documentos a recuperar

        Returns:
            Lista de tuplas (documento, score)
        """
        if not self.retriever:
            raise ValueError("Retriever no inicializado. Ejecuta rag_setup() primero.")

        return self.retriever.get_relevant_documents(
            question, k=similarity_score, filter_by_relevance=True
        )

    def load_documents(self):
        """Carga documentos desde el directorio configurado."""
        pass

    def rag_setup(self) -> None:
        """
        Configura todo el sistema RAG.

        Ejecuta el flujo completo: chunking -> vector store -> retriever
        """
        print("⚙️ Configurando sistema RAG...")

        # Generar chunks
        self.generate_chunks()
        print("🔹 Chunks generated successfully")

        # Crear vector store
        self.generate_vector_store()
        print("🔹 Vector store generated successfully")

        # Configurar evaluadora si está disponible
        if self.evaluadora:
            self.evaluadora.set_vector_store(self.vector_store)

        print("✅ Sistema RAG configurado correctamente")
