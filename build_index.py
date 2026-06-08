#!/usr/bin/env python3
"""Build the vector index from documents/."""

from src.index import build_index, preview_chunks


def main():
    stats = build_index()
    print(f"Indexed {stats['documents']} documents -> {stats['chunks']} chunks")
    print("\nSample chunks:")
    preview_chunks(5)


if __name__ == "__main__":
    main()
