from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.db.models import Conversation


class ConversationRepository:
    def create(
        self,
        db: Session,
        *,
        notebook_id: str,
        user_id: str,
        title: str,
    ) -> Conversation:
        conversation = Conversation(
            notebookId=notebook_id,
            userId=user_id,
            title=title,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def find_by_id(
        self,
        db: Session,
        *,
        id: str,
        user_id: str,
    ) -> Conversation | None:
        return db.scalar(
            select(Conversation).where(
                Conversation.id == id,
                Conversation.userId == user_id,
            )
        )

    def find_by_user(
        self,
        db: Session,
        *,
        user_id: str,
    ) -> list[Conversation]:
        return list(
            db.scalars(
                select(Conversation)
                .where(Conversation.userId == user_id)
                .order_by(Conversation.updatedAt.desc())
            )
        )

    def find_by_notebook(
        self,
        db: Session,
        *,
        notebook_id: str,
        user_id: str,
    ) -> list[Conversation]:
        return list(
            db.scalars(
                select(Conversation)
                .where(
                    Conversation.notebookId == notebook_id,
                    Conversation.userId == user_id,
                )
                .order_by(Conversation.updatedAt.desc())
            )
        )

    def delete(
        self,
        db: Session,
        *,
        id: str,
        user_id: str,
    ) -> int:
        result = db.execute(
            delete(Conversation).where(
                Conversation.id == id,
                Conversation.userId == user_id,
            )
        )

        db.commit()
        return result.rowcount or 0