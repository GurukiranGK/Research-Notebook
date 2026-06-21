from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from src.core.security import get_current_user
from src.schemas.search import SearchRequest
from src.services.search_service import search_chunks


router = APIRouter(prefix="/search", tags=["search"])


@router.post("")
def search_route(payload: SearchRequest, user: dict = Depends(get_current_user)):
    if not payload.documentId or not payload.query:
        raise HTTPException(status_code=400, detail="documentId and query are required")
    return jsonable_encoder(
        search_chunks(document_id=payload.documentId, user_id=user["id"], query=payload.query)
    )
