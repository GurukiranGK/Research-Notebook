from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.database import get_db
from src.repositories.document import DocumentRepository
from src.services.chunking_service import chunk_document


router = APIRouter(prefix="/chunks", tags=["chunks"])
document_repo = DocumentRepository()


@router.post("/{document_id}")
def chunk_document_route(
    document_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    document = document_repo.find_by_id(db, id=document_id, user_id=user["id"])
    if not document:
        return JSONResponse(status_code=404, content={"error": "Document not found"})

    result = chunk_document(db, document=document, user_id=user["id"])
    return {
        "message": "Document chunked",
        "chunksCreated": result["count"],
    }
