import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    port: int = int(os.getenv("PORT", "4000"))
    database_url: str = os.getenv("DATABASE_URL", "")

    keycloak_issuer: str = os.getenv("KEYCLOAK_ISSUER", "")
    keycloak_audience: str | None = os.getenv("KEYCLOAK_AUDIENCE")
    keycloak_client_id: str | None = (
        os.getenv("KEYCLOAK_CLIENT_ID")
        or os.getenv("KEYCLOAK_AUDIENCE")
    )
    keycloak_client_secret: str | None = os.getenv("KEYCLOAK_CLIENT_SECRET")
    keycloak_scope: str | None = os.getenv("KEYCLOAK_SCOPE", "openid")

    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "")


@lru_cache
def get_settings() -> Settings:
    return Settings()