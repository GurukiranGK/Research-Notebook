import httpx
from fastapi import HTTPException

from src.core.config import get_settings


def request_password_token(
    *,
    username: str,
    password: str,
) -> dict:
    settings = get_settings()

    if not settings.keycloak_issuer:
        raise HTTPException(
            status_code=500,
            detail="KEYCLOAK_ISSUER is missing"
        )

    if not settings.keycloak_client_id:
        raise HTTPException(
            status_code=500,
            detail="KEYCLOAK_CLIENT_ID is missing"
        )

    data = {
        "grant_type": "password",
        "client_id": settings.keycloak_client_id,
        "username": username,
        "password": password,
    }

    if settings.keycloak_client_secret:
        data["client_secret"] = settings.keycloak_client_secret

    if settings.keycloak_scope:
        data["scope"] = settings.keycloak_scope

    token_url = (
        f"{settings.keycloak_issuer}"
        "/protocol/openid-connect/token"
    )

    try:
        response = httpx.post(
            token_url,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            },
            timeout=15,
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not reach Keycloak: {exc}",
        ) from exc

    if response.status_code >= 400:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text

        raise HTTPException(
            status_code=response.status_code,
            detail=detail,
        )

    return response.json()