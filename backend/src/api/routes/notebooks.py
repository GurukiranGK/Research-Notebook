from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.database import get_db
from src.repositories.notebook import NotebookRepository
from src.schemas.notebook import NotebookCreate, NotebookOut, NotebookUpdate
from src.services.notebook_service import delete_notebook_with_children


router = APIRouter(prefix="/notebooks", tags=["notebooks"])
repo = NotebookRepository()


@router.post("", response_model=NotebookOut, status_code=201)
def create_notebook(
    payload: NotebookCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return repo.create(db, title=payload.title, user_id=user["id"])


@router.get("", response_model=list[NotebookOut])
def get_notebooks(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return repo.find_by_user(db, user["id"])


@router.put("/{notebook_id}")
def update_notebook(
    notebook_id: str,
    payload: NotebookUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    count = repo.update(db, id=notebook_id, user_id=user["id"], title=payload.title)
    if count == 0:
        return JSONResponse(status_code=404, content={"error": "Notebook not found"})
    return {"success": True}


@router.delete("/{notebook_id}")
def delete_notebook(
    notebook_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    count = delete_notebook_with_children(db, notebook_id=notebook_id, user_id=user["id"])
    if count == 0:
        return JSONResponse(status_code=404, content={"error": "Notebook not found"})
    return {"success": True}
