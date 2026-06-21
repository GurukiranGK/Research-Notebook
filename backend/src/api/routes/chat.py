from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.database import get_db
from src.schemas.chat import ChatRequest
from src.services.chat_service import chat_with_document


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
def chat_route(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    if not payload.documentId or not payload.question:
        raise HTTPException(status_code=400, detail="documentId and question required")
    return chat_with_document(
        db,
        document_id=payload.documentId,
        user_id=user["id"],
        question=payload.question,
    )
