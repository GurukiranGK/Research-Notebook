from typing import Annotated

import jwt
from fastapi import Header, HTTPException
from jwt import PyJWKClient

from src.core.config import get_settings


settings = get_settings()

if not settings.keycloak_issuer:
    raise RuntimeError("KEYCLOAK_ISSUER is missing")

jwks_client = PyJWKClient(f"{settings.keycloak_issuer}/protocol/openid-connect/certs")


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> dict:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid token")

    token = parts[1]
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        decoded = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings.keycloak_issuer,
            options={"verify_aud": False},
        )
    except Exception as exc:
        print("JWT error:", exc)
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    return {
        "id": decoded.get("sub"),
        "username": decoded.get("preferred_username"),
        "email": decoded.get("email"),
    }
