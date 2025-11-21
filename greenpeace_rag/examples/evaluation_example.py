
import os
import sys

# Agregar el directorio padre al path para importar el módulo original
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from greenpeace_rag import GreenpeaceRAG, RAGEvaluator
from greenpeace_rag.utils.config import get_chunking_params


def main():
    """Función principal del ejemplo de evaluación."""
    print("Evaluación del sistema RAG Greenpeace")
    print("=" * 60)
    
    # Configuración del sistema RAG
    print("📋 Configurando el sistema RAG...")
    
    chunk_strategy = "recursive_characters"
    chunk_params = get_chunking_params(chunk_strategy)
    
    # Crear instancia del RAG
    rag = GreenpeaceRAG(
        chunk_strategy=chunk_strategy,
        chunk_params=chunk_params
    )
    
    # Crear evaluador
    rag_evaluator = RAGEvaluator(rag)
    
    # Configurar el sistema RAG
    print("🔧 Configurando el sistema...")
    rag.rag_setup()
    
    print("\n🎯 Opciones de evaluación:")
    print("1. Generar contexto de evaluación (preguntas sintéticas)")
    print("2. Evaluar modelo completo")
    # print("3. Solo generar preguntas")
    # print("4. Solo generar respuestas")
    
    try:
        choice = input("\nSelecciona una opción (1-2): ").strip()
        
        if choice == "1":
            print("\n🔄 Generando contexto de evaluación...")
            amount = int(input("¿Cuántas preguntas generar? (por defecto 75): ") or "75")
            rag_evaluator.generate_evaluation_context(amount=amount)
            show_evaluation_results_questions()
            
        elif choice == "2":
            print("\n📈 Evaluando modelo completo...")
            rag_evaluator.evaluate_model()
            show_evaluation_results_model(rag_evaluator)
            
        # elif choice == "3":
        #     print("\n❓ Generando preguntas sintéticas...")
        #     amount = int(input("¿Cuántas preguntas generar? (por defecto 75): ") or "75")
        #     rag_evaluator.generate_synthetic_questions(amount=amount)
            
        # elif choice == "4":
        #     print("\n💭 Generando respuestas de evaluación...")
        #     rag_evaluator.generate_evaluation_answers()
            
        else:
            print("❌ Opción no válida")
            return
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Evaluación cancelada por el usuario")
        return
    except Exception as e:
        print(f"\n❌ Error durante la evaluación: {e}")
        return
    
    print("\n✅ Evaluación completada!")


def show_evaluation_results_questions():
    """Muestra los resultados de evaluación si existen."""
    try:
        import pickle
        
        if os.path.exists('evaluation_context.pkl'):
            with open('evaluation_context.pkl', 'rb') as f:
                questions = pickle.load(f)
            
            print(f"\n📊 Resumen de preguntas generadas:")
            print(f"   Total de preguntas: {len(questions)}")
            
            if questions and 'question_review_grade' in questions[0]:
                good_questions = [q for q in questions if q['question_review_grade'].score > 3]
                print(f"   Preguntas con score > 3: {len(good_questions)}")
                print(f"   Preguntas con score ≤ 3: {len(questions) - len(good_questions)}")
    except Exception as e:
        print(f"❌ Error mostrando resultados: {e}")

def show_evaluation_results_model(rag_evaluator):
    
    print(f"🔍 Resultados de la evaluación del modelo:")
    print(f"Correctness score: {rag_evaluator.correctness_score}")
    print(f"Relevance score: {rag_evaluator.relevance_score}")
    print(f"Groundness score: {rag_evaluator.groundness_score}")
    print(f"Retrieval relevance score: {rag_evaluator.retrieval_relevance_score}")


if __name__ == "__main__":
    main()
