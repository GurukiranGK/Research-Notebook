from fastapi import APIRouter, Depends, File, UploadFile,HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from src.services.document_services import delete_document_with_children


from src.core.security import get_current_user
from src.db.database import get_db
from src.repositories.document import DocumentRepository
from src.schemas.document import DocumentOut, DocumentUploadOut
from src.services.chunking_service import chunk_document
from src.utils.text_extractor import extract_text


router = APIRouter(prefix="/documents", tags=["documents"])
repo = DocumentRepository()


@router.post("/{notebook_id}", response_model=DocumentUploadOut, status_code=201)
async def upload_document(
    notebook_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    text = await extract_text(file)
    existing_document = repo.find_one_by_notebook(
        db,
        notebook_id=notebook_id,
        user_id=user["id"],
    )

    if existing_document:
        raise HTTPException(
            status_code=400,
            detail="This notebook already has a document",
        )
    document = repo.create(
        db,
        notebook_id=notebook_id,
        user_id=user["id"],
        filename=file.filename or "upload.txt",
        content=text,
    )
    result = chunk_document(db, document=document, user_id=user["id"])

    return {
        "id": document.id,
        "notebookId": document.notebookId,
        "userId": document.userId,
        "filename": document.filename,
        "content": document.content,
        "createdAt": document.createdAt,
        "chunksCreated": result["count"],
    }


@router.get("/{notebook_id}", response_model=list[DocumentOut])
def get_documents(
    notebook_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return repo.find_by_notebook(db, notebook_id=notebook_id, user_id=user["id"])

@router.delete("/{document_id}")
def delete_document(document_id:str,db: Session = Depends(get_db),user:dict=Depends(get_current_user)):
    count = delete_document_with_children(
        db,
        document_id=document_id,
        user_id=user["id"],
    )

    if count == 0:
        return JSONResponse(status_code=404, content={"error": "Document not found"})

    return {"success": True}
