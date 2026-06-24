from fastapi import APIRouter

from src.integrations.keycloak import request_password_token
from src.schemas.auth import TokenRequest, TokenResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.database import get_db
from src.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
)
from src.services.user_service import register_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def get_token(payload: TokenRequest):
    return request_password_token(
        username=payload.username,
        password=payload.password,
    )

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    return register_user(
        db,
        username=payload.username,
        email=payload.email,
        password=payload.password,
        display_name=payload.displayName,
    )