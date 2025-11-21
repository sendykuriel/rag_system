# RAG System - Greenpeace Documents

Un sistema completo de Retrieval-Augmented Generation (RAG) especializado en documentos de Greenpeace, desarrollado como parte del curso de LLMs del ITBA.

## 🌍 Descripción

Este proyecto proporciona un sistema RAG completo para hacer preguntas y obtener respuestas basadas en documentos de Greenpeace. El sistema incluye:

- **Chunking**: Múltiples estrategias para fragmentar documentos
- **Embedding**: Generación de embeddings usando modelos de sentence-transformers
- **Recuperación**: Búsqueda semántica de documentos relevantes
- **Generación**: Respuestas basadas en contexto usando LLMs locales (Ollama)
- **Evaluación**: Métricas completas para evaluar el rendimiento del sistema

## 📁 Estructura del Proyecto

```
.
├── greenpeace_rag/          # Paquete principal del sistema RAG
│   ├── core/                # Funcionalidades principales
│   ├── evaluation/          # Sistema de evaluación
│   ├── models/              # Configuración de modelos
│   ├── prompts/             # Prompts del sistema
│   ├── schemas/             # Modelos Pydantic
│   ├── utils/               # Utilidades compartidas
│   └── examples/            # Ejemplos de uso
├── docs/                    # Documentos fuente (PDFs, MDs)
├── docs_load_txt/           # Documentos procesados en formato TXT
├── chroma_db/               # Base de datos vectorial (ChromaDB)
├── clases/                  # Material del curso
└── pyproject.toml           # Configuración del proyecto
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.11+
- [Ollama](https://ollama.ai/) instalado y ejecutándose
- Modelo `llama3.1:8b` descargado en Ollama

### Pasos de Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/sendykuriel/rag_system.git
cd rag_system
```

2. **Crear y activar un entorno virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -e .
```

4. **Iniciar Ollama (en una terminal separada):**
```bash
ollama serve
```

5. **Descargar el modelo LLM (en otra terminal):**
```bash
ollama pull llama3.1:8b
```

## 📖 Uso Básico

### Ejemplo Simple

```python
from greenpeace_rag import GreenpeaceRAG

# Crear instancia del sistema RAG
rag = GreenpeaceRAG(
    chunk_strategy="recursive_characters",
    chunk_params={"chunk_char_size": 700, "chunk_overlap": 200}
)

# Configurar el sistema
rag.rag_setup()

# Hacer una pregunta
answer, context, docs = rag.generate_answers("¿Qué es el cambio climático?")
print(answer)
```

### Ejecutar Ejemplos

El proyecto incluye varios ejemplos en `greenpeace_rag/examples/`:

```bash
# Ejemplo básico
python greenpeace_rag/examples/basic_usage.py

# Ejemplo de evaluación
python greenpeace_rag/examples/evaluation_example.py
```

## 🔧 Configuración

### Estrategias de Chunking

- **`characters`**: Fragmentación simple por caracteres
- **`recursive_characters`**: Fragmentación recursiva (recomendado)
- **`documents_type`**: Adaptación según el tipo de documento

### Modelos Soportados

- **LLM**: Ollama con `llama3.1:8b` (por defecto)
- **Embeddings**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (por defecto)

## 📊 Evaluación

El sistema incluye un módulo completo de evaluación con las siguientes métricas:

- **Correctness**: Precisión de las respuestas generadas
- **Relevance**: Relevancia de las respuestas a las preguntas
- **Groundness**: Base de las respuestas en los documentos
- **Retrieval Relevance**: Relevancia de los documentos recuperados

Ver `greenpeace_rag/examples/evaluation_example.py` para más detalles.

## 🛠️ Desarrollo

Este proyecto está estructurado de forma modular para facilitar:

- **Mantenimiento**: Cada módulo tiene una responsabilidad específica
- **Extensibilidad**: Fácil agregar nuevas funcionalidades
- **Testing**: Componentes independientes
- **Reutilización**: Componentes pueden usarse por separado

## 📋 Requisitos

- Python >= 3.11
- Ollama instalado y ejecutándose
- Modelo `llama3.1:8b` descargado
- Dependencias listadas en `pyproject.toml`

## 🔗 Enlaces Útiles

- [Documentación de LangChain](https://python.langchain.com/)
- [Ollama](https://ollama.ai/)
- [Sentence Transformers](https://www.sbert.net/)
- [ChromaDB](https://www.trychroma.com/)

## 📄 Licencia

Este proyecto es parte del curso de LLMs del ITBA.

## 👤 Autor

Uriel Sendyk

