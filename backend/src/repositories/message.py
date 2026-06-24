from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import Message


class MessageRepository:
    def create(
        self,
        db: Session,
        *,
        conversation_id: str,
        role: str,
        content: str,
    ) -> Message:
        message = Message(
            conversationId=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def find_by_conversation(
        self,
        db: Session,
        *,
        conversation_id: str,
    ) -> list[Message]:
        return list(
            db.scalars(
                select(Message)
                .where(Message.conversationId == conversation_id)
                .order_by(Message.createdAt.asc())
            )
        )

    def find_recent(
        self,
        db: Session,
        *,
        conversation_id: str,
        limit: int = 10,
    ) -> list[Message]:
        messages = list(
            db.scalars(
                select(Message)
                .where(Message.conversationId == conversation_id)
                .order_by(Message.createdAt.desc())
                .limit(limit)
            )
        )

        messages.reverse()
        return messages