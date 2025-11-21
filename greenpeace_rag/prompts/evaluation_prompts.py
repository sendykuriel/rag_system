"""
Prompts para evaluación del sistema RAG.

Contiene todos los prompts utilizados en las diferentes métricas de evaluación.
"""

from langchain_core.prompts import PromptTemplate

# Prompt para generar preguntas sintéticas
QUESTION_GENERATION_PROMPT = PromptTemplate(
    input_variables=["context"],
    template="""<instructions>
Here is some context:
<context>
{context}
</context>
<role>You are a teacher creating a quiz from a given context.</role>
<task>
Your task is to generate 1 question that can be answered using the provided context, following these rules:

<rules>
1. The question should make sense to humans even when read without the given context.
2. The question should be fully answered from the given context.
3. The question should be framed from a part of context that contains important information. It can also be from tables, code, etc.
4. The answer to the question should not contain any links.
5. The question should be of moderate difficulty.
6. The question must be reasonable and must be understood and responded by humans.
7. Do not use phrases like 'provided context', etc. in the question.
8. Avoid framing questions using the word "and" that can be decomposed into more than one question.
9. The question should not contain more than 10 words, make use of abbreviations wherever possible.
</rules>

To generate the question, first identify the most important or relevant part of the context. Then frame a question around that part that satisfies all the rules above.

Output only the generated question with a "?" at the end, no other text or characters.
</task>
</instructions>"""
)


# Prompt para generar respuestas de evaluación
ANSWER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""<instructions>
<role>You are an experienced QA Engineer for building large language model applications.</role>
<task>
It is your task to generate an answer to the following question <question>{question}</question> only based on the <context>{context}</context></task>
The output should be only the answer generated from the context.

<rules>
1. Only use the given context as a source for generating the answer.
2. Be as precise as possible with answering the question.
3. Be concise in answering the question and only answer the question at hand rather than adding extra information.
</rules>

Only output the generated answer as a sentence. No extra characters.
</task>
</instructions>"""
)


# Prompt para revisión de preguntas (groundedness check)
QUESTION_REVIEW_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""<instructions>
<role>You are an experienced linguistics expert for building testsets for large language model applications.</role>

<task>
You will be given a context and a question related to that context.

Your task is to provide an evaluation of how well the given question can be answered using only the
information provided in the context.

<rules>
Rate this on a scale from 1 to 5, where:
1 = The question cannot be answered at all based on the given context
2 = The context provides very little relevant information to answer the question
3 = The context provides some relevant information to partially answer the question
4 = The context provides substantial information to answer most aspects of the question
5 = The context provides all the information needed to fully and unambiguously answer the question
</rules>

First, read through the provided context carefully:

<context>
{context}
</context>

Then read the question:

<question>
{question}
</question>

Evaluate how well you think the question can be answered using only the context information. 
Provide your reasoning first in an <evaluation> section, explaining what relevant or missing 
information from the context led you to your evaluation score in only one sentence.
</task>
</instructions>"""
)


# Prompt para evaluación de corrección
CORRECTNESS_EVALUATION_PROMPT = PromptTemplate(
    input_variables=["question", "ground_truth_answer", "answer"],
    template="""<instructions>
<role>You are a teacher grading a quiz.</role>
<task>
You will be given a QUESTION, the GROUND TRUTH (correct) ANSWER, and the STUDENT ANSWER.

<rules>
Here is the grade criteria to follow:
1. Grade the student answers based ONLY on their factual accuracy relative to the ground truth answer.
2. Ensure that the student answer does not contain any conflicting statements.
3. It is OK if the student answer contains more information than the ground truth answer, as long as it is factually accurate relative to the ground truth answer.

Here is the correctness criteria:
1. A correctness value of True means that the student's answer meets all of the criteria.
1. A correctness value of False means that the student's answer does not meet all of the criteria.
</rules>

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. Avoid simply stating the correct answer at the outset.

<question>
QUESTION:
{question}
</question>
<ground_truth_answer>
GROUND TRUTH ANSWER: {ground_truth_answer}
</ground_truth_answer>
<answer>
STUDENT ANSWER: {answer}
</answer>
</task>
</instructions>
"""
)


# Prompt para evaluación de relevancia
RELEVANCE_EVALUATION_PROMPT = PromptTemplate(
    input_variables=["question", "answer"],
    template="""<instrucions>
<role>You are a teacher grading a quiz. </role>
<task>
You will be given a QUESTION and a STUDENT ANSWER.

<rules>
Here is the grade criteria to follow:
1. Ensure the STUDENT ANSWER is concise and relevant to the QUESTION
2. Ensure the STUDENT ANSWER helps to answer the QUESTION

Here is the relevance criteria:
1. A relevance value of True means that the student's answer meets all of the criteria.
1. A relevance value of False means that the student's answer does not meet all of the criteria.
</rules>
Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. Avoid simply stating the correct answer at the outset.

<question>
QUESTION:
{question}
</question>
<answer>
STUDENT ANSWER: {answer}
</answer>
</task>
</instructions>
</task>
    </instrucions>"""
)


# Prompt para evaluación de groundedness
GROUNDEDNESS_EVALUATION_PROMPT = PromptTemplate(
    input_variables=["doc_string", "answer"],
    template="""<instructions>
<role>You are a teacher grading a quiz. </role>

<task>
You will be given FACTS and a STUDENT ANSWER.

<rules>
Here is the grade criteria to follow:
1. Ensure the STUDENT ANSWER is grounded in the FACTS.
2. Ensure the STUDENT ANSWER does not contain "hallucinated" information outside the scope of the FACTS.

Ans this is the grounded criteria:
1. A grounded value of True means that the student's answer meets all of the criteria.
2. A grounded value of False means that the student's answer does not meet all of the criteria.
</rules>

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct. Avoid simply stating the correct answer at the outset.

<facts>
FACTS:
{doc_string}
</facts>

<answer>
STUDENT ANSWER: {answer}
</answer>
</task>
</instructions>"""
)


# Prompt para evaluación de relevancia de recuperación
RETRIEVAL_RELEVANCE_PROMPT = PromptTemplate(
    input_variables=["doc_string", "question"],
    template="""<instructions>
<role>You are a teacher grading a quiz.</role>
<task>
Your task is to asses the revelance of a given QUESTION based on the FACTS provided by the student.

<rules>
Here is the grade criteria to follow:
1. You goal is to identify FACTS that are completely unrelated to the QUESTION
2. If the facts contain ANY keywords or semantic meaning related to the question, consider them relevant
3. It is OK if the facts have SOME information that is unrelated to the question as long as (2) is met

And this is the relevance criteria:

1. A relevance value of True means that the FACTS contain ANY keywords or 
semantic meaning related to the QUESTION and are therefore relevant.
2. A relevance value of False means that the FACTS are completely unrelated to the QUESTION.
</rules>

Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct.
Avoid simply stating the correct answer at the outset.

Here are the facts:
<facts>
{doc_string}
</facts>

And this is the question:
<question>{question}</question>
</task>
</instructions>"""
)
