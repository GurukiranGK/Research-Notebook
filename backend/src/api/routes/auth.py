from fastapi import APIRouter

from src.integrations.keycloak import request_password_token
from src.schemas.auth import TokenRequest, TokenResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def get_token(payload: TokenRequest):
    return request_password_token(
        username=payload.username,
        password=payload.password,
    )
