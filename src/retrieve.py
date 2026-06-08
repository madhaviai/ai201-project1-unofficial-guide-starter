from src.config import TOP_K
from src.index import get_collection


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """Return top-k relevant chunks with source metadata and distance."""
    collection = get_collection()
    results = collection.query(query_texts=[query], n_results=top_k)

    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append(
            {
                "text": text,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "distance": distance,
            }
        )
    return chunks
