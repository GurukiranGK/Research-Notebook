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
    MessageCreate,
    ConversationMessageResponse
)
from src.services.chat_service import chat_with_document
from src.services.answer_service import summarize_conversation
from src.repositories.document import DocumentRepository
from src.services.answer_service import  generate_conversation_title

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
)

conversation_repo = ConversationRepository()
document_repo = DocumentRepository()
message_repo = MessageRepository()

@router.post(
    "/{conversation_id}/messages",response_model=ConversationMessageResponse,
    status_code=201,
)
def create_message(
    conversation_id: str,
    payload: MessageCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
) -> ConversationMessageResponse:
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

    document = document_repo.find_one_by_notebook(
        db,
        notebook_id=conversation.notebookId,
        user_id=user["id"],
    )
    
    if not document:
        raise HTTPException(
        status_code=404,
        detail="Document not found",
    )

    if document.notebookId != conversation.notebookId:
        raise HTTPException(
        status_code=400,
        detail="Document does not belong to this conversation notebook",
    )
        
    user_message = message_repo.create(
        db,
        conversation_id=conversation_id,
        role="user",
        content=payload.content,
    )
    
    generated_title=conversation.title
    
    if conversation.title == "New conversation":
        generated_title = generate_conversation_title(
            user_message=user_message.content,
        )

    conversation_repo.update_title(
        db,
        id=conversation_id,
        user_id=user["id"],
        title=generated_title,
    )

    result = chat_with_document(
        db,
        document_id=document.id,
        user_id=user["id"],
        question=payload.content,
        conversation_summary=conversation.summary,
    )

    assistant_message = message_repo.create(
        db,
        conversation_id=conversation_id,
        role="assistant",
        content=result["answer"],
    )

    updated_summary = summarize_conversation(
        old_summary=conversation.summary,
        user_message=user_message.content,
        assistant_message=assistant_message.content,
    )

    conversation_repo.update_summary(
        db,
        id=conversation_id,
        user_id=user["id"],
        summary=updated_summary,
    )

    return {
        "userMessage": MessageOut.model_validate(user_message),
        "assistantMessage": MessageOut.model_validate(assistant_message),
        "answer": result["answer"],
        "sources": result["sources"],
        "summary": updated_summary,
        "title" : generated_title
    }

@router.post(
    "/{conversation_id}/messages",
    response_model=MessageOut,
    status_code=201,
)
def create_message(
    conversation_id: str,
    payload: MessageCreate,
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

    return message_repo.create(
        db,
        conversation_id=conversation_id,
        role="user",
        content=payload.content,
    )


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