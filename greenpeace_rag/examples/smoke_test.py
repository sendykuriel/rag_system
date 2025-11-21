"""
Smoke test mínimo para validar setup del RAG.
"""

from greenpeace_rag import GreenpeaceRAG


def main():
    rag = GreenpeaceRAG(
        txt_dir="/Users/urielsendyk/Documents/itba/13 LLMs/docs_load_txt",
        chroma_db_path="./chroma_db",
        collection_name="greenpeace_docs",
        chunk_strategy="recursive_characters",
    )

    rag.rag_setup()

    question = "¿Qué es Greenpeace?"
    answer, _, _ = rag.generate_answers(question, similarity_score=1)
    assert isinstance(answer, str)
    print("Smoke test OK")


if __name__ == "__main__":
    main()


