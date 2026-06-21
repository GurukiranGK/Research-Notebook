from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from src.db.models import Notebook


class NotebookRepository:
    def create(self, db: Session, *, title: str, user_id: str) -> Notebook:
        notebook = Notebook(title=title, userId=user_id)
        db.add(notebook)
        db.commit()
        db.refresh(notebook)
        return notebook

    def find_by_user(self, db: Session, user_id: str) -> list[Notebook]:
        return list(
            db.scalars(
                select(Notebook)
                .where(Notebook.userId == user_id)
                .order_by(Notebook.createdAt.desc())
            )
        )

    def find_by_id(self, db: Session, *, id: str, user_id: str) -> Notebook | None:
        return db.scalar(select(Notebook).where(Notebook.id == id, Notebook.userId == user_id))

    def update(self, db: Session, *, id: str, user_id: str, title: str) -> int:
        result = db.execute(
            update(Notebook)
            .where(Notebook.id == id, Notebook.userId == user_id)
            .values(title=title)
        )
        db.commit()
        return result.rowcount or 0

    def delete(self, db: Session, *, id: str, user_id: str) -> int:
        result = db.execute(delete(Notebook).where(Notebook.id == id, Notebook.userId == user_id))
        db.commit()
        return result.rowcount or 0
