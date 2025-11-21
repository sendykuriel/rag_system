"""
Prompts para el sistema RAG principal.

Contiene los prompts utilizados para generar respuestas y filtrar documentos.
"""

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# Prompt para el sistema RAG principal
RAG_SYSTEM_PROMPT = """Eres un asistente experto en temas ambientales y de Greenpeace.

Tu tarea es responder preguntas basándote ÚNICAMENTE en el contexto proporcionado.

Reglas importantes:
- Si la información NO está en el contexto, di "No tengo información suficiente en los documentos para responder eso."
- Cita las fuentes cuando sea relevante (menciona de qué documento viene la información)
- Sé preciso y objetivo
- Si encuentras información contradictoria, mencionalo
- Debes responder en el idioma que el usuario te pregunta.

Contexto de los documentos:
{context}"""


def get_rag_chat_prompt():
    """Obtiene el prompt template para el chat RAG."""
    return ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_PROMPT),
        ("human", "{question}")
    ])


# Prompt para filtrado de documentos por relevancia
DOCUMENT_FILTER_PROMPT = PromptTemplate(
    input_variables=["question", "context"],
    template="""<instrucions>
<role>You are a teacher grading a quiz. </role>
<task>
You will be given a QUESTION and a CONTEXT.

<rules>
Here is the grade criteria to follow:
1. Ensure the CONTEXT is concise and relevant to the QUESTION
2. Ensure the CONTEXT helps to answer the QUESTION

Here is the relevance criteria:
1. A relevance value of True means that given context meets all of the criteria.
1. A relevance value of False means that the given context does not meet all of the criteria.
</rules>

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. Avoid simply stating the correct answer at the outset.

<context>
Context: {context}
</context>

<question>
QUESTION:
{question}
</question>

</task>
</instructions>
</task>
    </instrucions>"""
)

KEYWORDS_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""<instrucions>
<role>You are a teacher grading a quiz. </role>
<task>
You will be given a QUESTION.

<question>
QUESTION:
{question}
</question>
</task>
</instructions>"""
)

RANKING_PROMPT = PromptTemplate(
    input_variables=["question", "amount"],
    template="""<instructions>
<role>You are a helpful AI language model assistant that generates multiple search queries based on a single input query.</role>
<task>
Your task is to generate {amount} different versions of the given user question to retrieve relevant documents from a vector database.
By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of the distance-based similarity search.
<question>
Question: {question}
</question>
</task>
</instructions>""")