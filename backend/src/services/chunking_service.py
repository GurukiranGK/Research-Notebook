from sqlalchemy.orm import Session

from src.db.models import Document
from src.repositories.chunk import ChunkRepository
from src.utils.chunker import chunk_text
from .indexing_service import index_chunks
from .vector_service import delete_document_vectors


repo = ChunkRepository()


def chunk_document(db: Session, *, document: Document, user_id: str) -> dict:
    delete_document_vectors(document_id=document.id, user_id=user_id)
    repo.delete_by_document(db, document_id=document.id, user_id=user_id)

    chunks = chunk_text(document.content)
    print("Chunks:", len(chunks))
    print("First chunk content:", chunks[0]["content"] if chunks else None)
    print("Content length:", len(chunks[0]["content"]) if chunks else None)

    repo.bulk_create(db, document_id=document.id, user_id=user_id, chunks=chunks)
    stored_chunks = repo.find_by_document(db, document_id=document.id, user_id=user_id)
    index_chunks(chunks=stored_chunks)

    return {"count": len(stored_chunks)}
