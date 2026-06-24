from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import User


class UserRepository:
    def create(
        self,
        db: Session,
        *,
        id: str,
        username: str,
        email: str,
        display_name: str | None,
    ) -> User:
        user = User(
            id=id,
            username=username,
            email=email,
            displayName=display_name,
        )
        db.add(user)
        db.flush()
        return user

    def find_by_id(self, db: Session, *, id: str) -> User | None:
        return db.scalar(select(User).where(User.id == id))