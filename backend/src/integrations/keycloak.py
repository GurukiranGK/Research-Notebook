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

def get_admin_token() -> str:
    settings = get_settings()

    response = httpx.post(
        f"{settings.keycloak_issuer}/protocol/openid-connect/token",
        data={
            "grant_type": "client_credentials",
            "client_id": settings.keycloak_admin_client_id,
            "client_secret": settings.keycloak_admin_client_secret,
        },
        timeout=15,
    )

    if response.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail="Could not authenticate with Keycloak Admin API",
        )

    return response.json()["access_token"]


def get_admin_users_url() -> str:
    settings = get_settings()

    if "/realms/" not in settings.keycloak_issuer:
        raise HTTPException(
            status_code=500,
            detail="Invalid KEYCLOAK_ISSUER",
        )

    base_url, realm = settings.keycloak_issuer.rsplit("/realms/", 1)
    return f"{base_url}/admin/realms/{realm}/users"


def create_keycloak_user(
    *,
    username: str,
    email: str,
    password: str,
) -> str:
    token = get_admin_token()

    response = httpx.post(
        get_admin_users_url(),
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": username,
            "email": email,
            "enabled": True,
            "emailVerified": False,
            "credentials": [
                {
                    "type": "password",
                    "value": password,
                    "temporary": False,
                }
            ],
        },
        timeout=15,
    )

    if response.status_code == 409:
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    if response.status_code != 201:
        raise HTTPException(
            status_code=502,
            detail=f"Keycloak user creation failed: {response.text}",
        )

    return response.headers["Location"].rstrip("/").split("/")[-1]


def delete_keycloak_user(user_id: str) -> None:
    token = get_admin_token()

    httpx.delete(
        f"{get_admin_users_url()}/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )