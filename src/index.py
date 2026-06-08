import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from typing import Optional

from src.chunk import chunk_documents
from src.config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL
from src.ingest import load_documents


def get_embedding_function() -> SentenceTransformerEmbeddingFunction:
    return SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)


def get_client() -> chromadb.PersistentClient:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection(client: Optional[chromadb.ClientAPI] = None):
    client = client or get_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )


def build_index() -> dict:
    """Load docs, chunk, embed, and store in ChromaDB."""
    documents = load_documents()
    chunks = chunk_documents(documents)

    client = get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = get_collection(client)

    ids = []
    texts = []
    metadatas = []
    for i, chunk in enumerate(chunks):
        ids.append(f"{chunk['source']}::{chunk['chunk_index']}")
        texts.append(chunk["text"])
        metadatas.append(
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    collection.add(ids=ids, documents=texts, metadatas=metadatas)

    return {
        "documents": len(documents),
        "chunks": len(chunks),
    }


def preview_chunks(n: int = 5) -> None:
    """Print sample chunks for Milestone 3 inspection."""
    documents = load_documents()
    chunks = chunk_documents(documents)
    print(f"Total documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}\n")
    for chunk in chunks[:n]:
        print(f"--- {chunk['source']} [chunk {chunk['chunk_index']}] ---")
        print(chunk["text"])
        print()
