from sqlalchemy.orm import Session

from src.repositories.chunk import ChunkRepository
from src.repositories.document import DocumentRepository
from src.services.vector_service import delete_document_vectors

document_repo = DocumentRepository()
chunk_repo = ChunkRepository()

def delete_document_with_children(db: Session, *, document_id: str, user_id: str) -> int:
    document = document_repo.find_by_id(db, id=document_id, user_id=user_id)
    if not document:
        return 0

    delete_document_vectors(document_id=document_id, user_id=user_id)
    chunk_repo.delete_by_document(db, document_id=document_id, user_id=user_id)

    return document_repo.delete(db, id=document_id, user_id=user_id)