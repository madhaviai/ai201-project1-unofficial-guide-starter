#!/usr/bin/env python3
"""Run all 5 evaluation questions and print results for README."""

from src.query import ask

EVAL_QUESTIONS = [
    "How does the professor grade dynamic programming questions?",
    "Can I use Dijkstra's algorithm when the graph has negative edge weights?",
    "What are the rules for the AI Search Agent project autograder?",
    "Is attendance graded in CS 482?",
    "What was the Fall 2024 midterm average score?",
]


def main():
    for i, question in enumerate(EVAL_QUESTIONS, 1):
        print("=" * 70)
        print(f"Q{i}: {question}\n")
        result = ask(question)
        print("ANSWER:")
        print(result["answer"])
        print("\nSOURCES:")
        for source in result["sources"]:
            print(f"  - {source}")
        print("\nTOP CHUNKS:")
        for chunk in result["chunks"][:3]:
            print(f"  - {chunk['source']} (distance: {chunk['distance']:.3f})")
        print()


if __name__ == "__main__":
    main()
