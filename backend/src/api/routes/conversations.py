from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.core.security import get_current_user
from src.db.database import get_db
from src.repositories.conversation import ConversationRepository
from src.repositories.message import MessageRepository
from src.schemas.conversation import (
    ConversationCreate,
    ConversationOut,
    MessageOut,
)


router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)

conversation_repo = ConversationRepository()
message_repo = MessageRepository()


@router.post("", response_model=ConversationOut, status_code=201)
def create_conversation(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return conversation_repo.create(
        db,
        notebook_id=payload.notebookId,
        user_id=user["id"],
        title=payload.title,
    )


@router.get("", response_model=list[ConversationOut])
def get_conversations(
    notebook_id: str | None = Query(default=None, alias="notebookId"),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    if notebook_id:
        return conversation_repo.find_by_notebook(
            db,
            notebook_id=notebook_id,
            user_id=user["id"],
        )

    return conversation_repo.find_by_user(
        db,
        user_id=user["id"],
    )


@router.get("/{conversation_id}", response_model=ConversationOut)
def get_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    conversation = conversation_repo.find_by_id(
        db,
        id=conversation_id,
        user_id=user["id"],
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return conversation


@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageOut],
)
def get_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    conversation = conversation_repo.find_by_id(
        db,
        id=conversation_id,
        user_id=user["id"],
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return message_repo.find_by_conversation(
        db,
        conversation_id=conversation_id,
    )


@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    deleted = conversation_repo.delete(
        db,
        id=conversation_id,
        user_id=user["id"],
    )

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {"success": True}