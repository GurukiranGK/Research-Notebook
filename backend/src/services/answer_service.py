from src.db.models import Chunk
from src.integrations.gemini import get_llm


def answer_question(*, question: str, chunks: list[Chunk]) -> str:
    context = "\n\n".join(
        f"Chunk {index + 1}:\n{chunk.content}" for index, chunk in enumerate(chunks)
    )

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}

Answer:
"""

    response = get_llm().invoke(prompt)
    return response.content
