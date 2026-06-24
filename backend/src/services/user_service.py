from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.integrations.keycloak import (
    create_keycloak_user,
    delete_keycloak_user,
)
from src.repositories.user import UserRepository

user_repo = UserRepository()


def register_user(
    db: Session,
    *,
    username: str,
    email: str,
    password: str,
    display_name: str | None,
):
    keycloak_user_id = create_keycloak_user(
        username=username,
        email=email,
        password=password,
    )

    try:
        user = user_repo.create(
            db,
            id=keycloak_user_id,
            username=username,
            email=email,
            display_name=display_name,
        )
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError as exc:
        db.rollback()
        delete_keycloak_user(keycloak_user_id)

        raise HTTPException(
            status_code=409,
            detail="User already exists",
        ) from exc

    except Exception:
        db.rollback()
        delete_keycloak_user(keycloak_user_id)
        raise