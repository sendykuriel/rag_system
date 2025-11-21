# Greenpeace RAG Package

Un sistema de Retrieval-Augmented Generation (RAG) especializado en documentos de Greenpeace.

## 🌍 Descripción

Este paquete proporciona un sistema RAG completo para hacer preguntas y obtener respuestas basadas en documentos de Greenpeace. Incluye funcionalidades para:

- **Chunking**: Diferentes estrategias para fragmentar documentos
- **Embedding**: Generación de embeddings usando modelos de sentence-transformers
- **Recuperación**: Búsqueda semántica de documentos relevantes
- **Generación**: Respuestas basadas en contexto usando LLMs
- **Evaluación**: Métricas completas para evaluar el rendimiento

## 📁 Estructura del Paquete

```
greenpeace_rag/
├── core/                    # Funcionalidades principales
│   ├── chunking/           # Estrategias de fragmentación
│   └── retrieval/          # Recuperación y filtrado
├── evaluation/             # Sistema de evaluación
│   ├── metrics/            # Métricas de evaluación
│   └── question_generation/ # Generación de preguntas sintéticas
├── models/                 # Configuración de modelos
├── prompts/                # Prompts del sistema
├── schemas/                # Modelos Pydantic
├── utils/                  # Utilidades compartidas
└── examples/               # Ejemplos de uso
```

## 🚀 Instalación

```bash
# Clonar o descargar el paquete
cd greenpeace_rag

# Instalar dependencias
pip install -r requirements.txt

# Asegurar que Ollama esté ejecutándose
ollama serve
```

## 📖 Uso Básico

```python
from greenpeace_rag import GreenpeaceRAG

# Configurar el sistema
rag = GreenpeaceRAG(
    chunk_strategy="recursive_characters",
    chunk_params={"chunk_char_size": 1000}
)

# Configurar el sistema RAG
rag.rag_setup()

# Hacer una pregunta
answer, context, docs = rag.generate_answers("¿Qué es el cambio climático?")
print(answer)
```

## 🔧 Configuración

### Estrategias de Chunking

- **`characters`**: Fragmentación por caracteres
- **`recursive_characters`**: Fragmentación recursiva (recomendado)
- **`semantic`**: Fragmentación semántica

### Modelos Soportados

- **LLM**: Ollama (llama3.1:8b por defecto)
- **Embeddings**: sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2)

## 📊 Evaluación

El sistema incluye métricas de evaluación:

- **Correctness**: Precisión de las respuestas
- **Relevance**: Relevancia de las respuestas
- **Groundness**: Base en documentos
- **Retrieval Relevance**: Relevancia de documentos recuperados

```python
from greenpeace_rag import RAGEvaluator

evaluator = RAGEvaluator(rag)
evaluator.evaluate_model()
```

## 📝 Ejemplos

Ver la carpeta `examples/` para ejemplos detallados:

- `basic_usage.py`: Uso básico del sistema
- `evaluation_example.py`: Evaluación del rendimiento

## 🛠️ Desarrollo

### Estructura Modular

El paquete está diseñado de forma modular para facilitar:

- **Mantenimiento**: Cada módulo tiene una responsabilidad específica
- **Extensibilidad**: Fácil agregar nuevas funcionalidades
- **Testing**: Componentes independientes para testing
- **Reutilización**: Componentes pueden usarse por separado

### Migración Gradual

El paquete se está desarrollando de forma gradual:

1. ✅ Estructura de carpetas creada
2. ✅ Modelos Pydantic extraídos
3. ✅ Prompts organizados
4. ✅ Utilidades básicas creadas
5. ✅ Ejemplos de uso creados
6. 🔄 Migración de clases principales (pendiente)

## 📋 Requisitos

- Python 3.8+
- Ollama (para LLM local)
- Dependencias en `requirements.txt`

## 🤝 Contribución

Para contribuir al desarrollo:

1. Mantener la estructura modular
2. Documentar nuevas funcionalidades
3. Agregar tests para nuevos componentes
4. Seguir las convenciones de naming

## 📄 Licencia

Este proyecto es parte del curso de LLMs del ITBA.

## 🔗 Enlaces Útiles

- [Documentación de LangChain](https://python.langchain.com/)
- [Ollama](https://ollama.ai/)
- [Sentence Transformers](https://www.sbert.net/)
