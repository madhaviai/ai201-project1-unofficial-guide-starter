from src.config import CHUNK_OVERLAP, CHUNK_SIZE


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[dict]:
    """Split text into fixed-size overlapping chunks with metadata."""
    if not text:
        return []

    if len(text) <= chunk_size:
        return [
            {
                "text": text,
                "source": source,
                "chunk_index": 0,
            }
        ]

    chunks = []
    start = 0
    index = 0
    while start < len(text):
        end = start + chunk_size
        piece = text[start:end].strip()
        if piece:
            chunks.append(
                {
                    "text": piece,
                    "source": source,
                    "chunk_index": index,
                }
            )
            index += 1
        if end >= len(text):
            break
        start = end - overlap

    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chunk all loaded documents."""
    all_chunks = []
    for doc in documents:
        all_chunks.extend(chunk_text(doc["text"], doc["source"]))
    return all_chunks
