import os

from dotenv import load_dotenv
from groq import Groq

from src.config import LLM_MODEL

load_dotenv()

SYSTEM_PROMPT = """You are a course assistant for CS 482 Applied Algorithms.

Answer the user's question using ONLY the provided document excerpts.
Do not use outside knowledge.
If the excerpts do not contain enough information, respond exactly with:
"I don't have enough information on that."

Requirements:
- Ground every claim in the excerpts.
- Mention source filenames when stating facts.
- Be concise and student-friendly.
"""


def format_context(chunks: list[dict]) -> str:
    blocks = []
    for chunk in chunks:
        blocks.append(
            f"[Source: {chunk['source']} | chunk {chunk['chunk_index']}]\n{chunk['text']}"
        )
    return "\n\n---\n\n".join(blocks)


def generate_answer(question: str, chunks: list[dict]) -> str:
    if not chunks:
        return "I don't have enough information on that."

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    context = format_context(chunks)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Documents:\n{context}\n\nQuestion: {question}",
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
