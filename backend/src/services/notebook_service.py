from sqlalchemy.orm import Session

from src.repositories.chunk import ChunkRepository
from src.repositories.document import DocumentRepository
from src.repositories.notebook import NotebookRepository
from src.services.vector_service import delete_document_vectors


notebook_repo = NotebookRepository()
document_repo = DocumentRepository()
chunk_repo = ChunkRepository()


def delete_notebook_with_children(db: Session, *, notebook_id: str, user_id: str) -> int:
    notebook = notebook_repo.find_by_id(db, id=notebook_id, user_id=user_id)
    if not notebook:
        return 0

    documents = document_repo.find_by_notebook(
        db,
        notebook_id=notebook_id,
        user_id=user_id,
    )

    for document in documents:
        delete_document_vectors(document_id=document.id, user_id=user_id)
        chunk_repo.delete_by_document(db, document_id=document.id, user_id=user_id)

    document_repo.delete_by_notebook(db, notebook_id=notebook_id, user_id=user_id)
    return notebook_repo.delete(db, id=notebook_id, user_id=user_id)
