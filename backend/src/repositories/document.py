from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.db.models import Document


class DocumentRepository:
    def create(
        self,
        db: Session,
        *,
        notebook_id: str,
        user_id: str,
        filename: str,
        content: str,
    ) -> Document:
        document = Document(
            notebookId=notebook_id,
            userId=user_id,
            filename=filename,
            content=content,
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    def find_by_notebook(self, db: Session, *, notebook_id: str, user_id: str) -> list[Document]:
        return list(
            db.scalars(
                select(Document)
                .where(Document.notebookId == notebook_id, Document.userId == user_id)
                .order_by(Document.createdAt.desc())
            )
        )

    def find_by_id(self, db: Session, *, id: str, user_id: str) -> Document | None:
        return db.scalar(select(Document).where(Document.id == id, Document.userId == user_id))

    def delete_by_notebook(self, db: Session, *, notebook_id: str, user_id: str) -> int:
        result = db.execute(
            delete(Document).where(Document.notebookId == notebook_id, Document.userId == user_id)
        )
        db.commit()
        return result.rowcount or 0
    
    def delete(self, db: Session, *, id: str, user_id: str) -> int:
        result = db.execute(
            delete(Document).where(
            Document.id == id,
            Document.userId == user_id,
        )
        )
        db.commit()
        return result.rowcount or 0
