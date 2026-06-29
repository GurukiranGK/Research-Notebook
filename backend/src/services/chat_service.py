from sqlalchemy.orm import Session

from src.repositories.chunk import ChunkRepository
from .answer_service import answer_question
from .search_service import search_chunks


chunk_repo = ChunkRepository()


def chat_with_document(
    db: Session,
    *,
    document_id: str,
    user_id: str,
    question: str,
    conversation_summary: str | None = None,
) -> dict:
    results = search_chunks(
    document_id=document_id,
    user_id=user_id,
    query=question,
    limit=5,
    )

    chunk_ids = [
    result.metadata["chunkId"]
    for result in results
    ]

    chunks = chunk_repo.find_by_ids(
        db,
        ids=chunk_ids,
        user_id=user_id,
        document_id=document_id,
    )

    chunks_by_id = {chunk.id: chunk for chunk in chunks}

    ordered_chunks = [
        chunks_by_id[chunk_id]
        for chunk_id in chunk_ids
        if chunk_id in chunks_by_id
    ]

    if not ordered_chunks:
        return {
            "answer": "I don't know. No matching source chunks were found in the database for this document.",
            "sources": chunk_ids,
        }

    answer = answer_question(
        question=question,
        chunks=ordered_chunks,
        conversation_summary=conversation_summary,
    )

    return {
        "answer": answer,
        "sources": [chunk.id for chunk in ordered_chunks],
    }