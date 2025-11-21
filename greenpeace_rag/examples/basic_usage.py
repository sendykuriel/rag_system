"""
Ejemplo básico de uso de GreenpeaceRAG.
"""

from greenpeace_rag import GreenpeaceRAG
from greenpeace_rag.utils.config import get_chunking_params


def main():
    rag = GreenpeaceRAG(
        llm_provider="ollama",
        llm_model="llama3.1:8b",
        txt_dir="/Users/urielsendyk/Documents/itba/13 LLMs/docs_load_txt",
        chroma_db_path="./chroma_db",
        collection_name="greenpeace_docs",
        embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        chunk_strategy="recursive_characters",
    )

    rag.rag_setup()

    question = "¿Qué es el cambio climático?"
    answer, context, docs = rag.generate_answers(question, similarity_score=3)
    print("Pregunta:", question)
    print("Respuesta:\n", answer)


if __name__ == "__main__":
    main()

"""
Ejemplo básico de uso del sistema Greenpeace RAG.

Este ejemplo muestra cómo usar el sistema RAG para hacer preguntas
sobre documentos de Greenpeace.
"""

# Nota: Este ejemplo asume que el código original se ha migrado al paquete
# Por ahora, importamos desde el archivo original para demostrar el uso

import os
import sys

# Agregar el directorio padre al path para importar el módulo original
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from greenpeace_rag import GreenpeaceRAG


def main():
    """Función principal del ejemplo."""
    print("🌍 Ejemplo de uso del sistema Greenpeace RAG")
    print("=" * 50)
    
    # Configuración del sistema RAG
    print("📋 Configurando el sistema RAG...")
    
    # Configuración de chunking
    chunk_strategy = "recursive_characters"
    chunk_params = get_chunking_params(chunk_strategy)
    
    # Crear instancia del RAG
    rag = GreenpeaceRAG(
        chunk_strategy=chunk_strategy,
        chunk_params=chunk_params
    )
    
    # Configurar el sistema RAG
    print("🔧 Configurando el sistema...")
    rag.rag_setup()
    
    # Ejemplos de preguntas
    questions = [
        "¿Qué es el cambio climático?",
        "¿Cuáles son las principales amenazas para los océanos?",
        "¿Qué hace Greenpeace para proteger el medio ambiente?",
        "¿Cuáles son los efectos de la deforestación?",
        "¿Qué es la energía renovable?"
    ]
    
    print("\n❓ Haciendo preguntas al sistema RAG:")
    print("-" * 50)
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Pregunta: {question}")
        print("   Respuesta:")
        
        try:
            # Generar respuesta
            answer, context, docs_with_scores = rag.generate_answers(question)
            
            # Mostrar respuesta
            print(f"   {answer}")
            
            # Mostrar información de los documentos utilizados
            print(f"   📄 Documentos utilizados: {len(docs_with_scores)}")
            for j, (doc, score) in enumerate(docs_with_scores, 1):
                print(f"      {j}. {doc.metadata.get('file_name', 'Unknown')} (score: {score:.3f})")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Ejemplo completado!")


if __name__ == "__main__":
    main()
