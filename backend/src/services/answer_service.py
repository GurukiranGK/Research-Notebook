from src.db.models import Chunk
from src.integrations.gemini import get_llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful research assistant.

Use the conversation summary only to understand the user's previous intent.
Use the document context to answer the current question.

If the answer is not in the document context, say you don't know.
""",
        ),
        (
            "human",
            """
Conversation summary:
{conversation_summary}

Document context:
{context}

Current question:
{question}

Answer:
""",
        ),
    ]
)

summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You maintain a short memory summary for a chat conversation.

Keep only important context that helps future answers.
Do not include unnecessary details.
Keep it concise.
""",
        ),
        (
            "human",
            """
Previous summary:
{old_summary}

Latest user message:
{user_message}

Latest assistant response:
{assistant_message}

Updated summary:
""",
        ),
    ]
)

title_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Generate a short title for a chat conversation.

Rules:
- Maximum 5 words
- No quotation marks
- No punctuation at the end
- Title case
""",
        ),
        (
            "human",
            """
User message:
{user_message}

Title:
""",
        ),
    ]
)


def _chain(prompt: ChatPromptTemplate):
    return prompt | get_llm() | StrOutputParser()


def answer_question(
    *,
    question: str,
    chunks: list[Chunk],
    conversation_summary: str | None = None,
) -> str:
    context = "\n\n".join(
        f"Chunk {index + 1}:\n{chunk.content}"
        for index, chunk in enumerate(chunks)
    )

    summary_text = conversation_summary or "No previous conversation summary."

    return _chain(answer_prompt).invoke(
        {
            "conversation_summary": summary_text,
            "context": context,
            "question": question,
        }
    )


def summarize_conversation(
    *,
    old_summary: str | None,
    user_message: str,
    assistant_message: str,
) -> str:
    previous_summary = old_summary or "No previous summary."

    return _chain(summary_prompt).invoke(
        {
            "old_summary": previous_summary,
            "user_message": user_message,
            "assistant_message": assistant_message,
        }
    )

def generate_conversation_title(*, user_message: str) -> str:
    title = _chain(title_prompt).invoke({"user_message": user_message}).strip()

    if not title:
        return "New conversation"

    return title[:80]
