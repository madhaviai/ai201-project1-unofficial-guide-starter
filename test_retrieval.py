#!/usr/bin/env python3
"""Test retrieval on 3 evaluation queries (Milestone 4)."""

from src.retrieve import retrieve

TEST_QUERIES = [
    "How does the professor grade dynamic programming questions?",
    "Can I use Dijkstra's algorithm when the graph has negative edge weights?",
    "What are the rules for the AI Search Agent project autograder?",
]


def main():
    for query in TEST_QUERIES:
        print("=" * 70)
        print(f"QUERY: {query}\n")
        chunks = retrieve(query)
        for i, chunk in enumerate(chunks, 1):
            print(f"[{i}] {chunk['source']} (distance: {chunk['distance']:.3f})")
            print(chunk["text"][:200] + ("..." if len(chunk["text"]) > 200 else ""))
            print()


if __name__ == "__main__":
    main()
