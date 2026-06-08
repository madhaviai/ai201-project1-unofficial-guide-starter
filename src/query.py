from src.generate import generate_answer
from src.retrieve import retrieve


def ask(question: str) -> dict:
    """End-to-end RAG: retrieve chunks, generate grounded answer, return sources."""
    chunks = retrieve(question)
    answer = generate_answer(question, chunks)
    sources = sorted({chunk["source"] for chunk in chunks})
    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks,
    }
