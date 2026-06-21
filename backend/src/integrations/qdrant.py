from functools import lru_cache

from qdrant_client import QdrantClient

from src.core.config import get_settings


settings = get_settings()

if not settings.qdrant_url:
    raise RuntimeError("QDRANT_URL is missing")


@lru_cache
def get_qdrant() -> QdrantClient:
    return QdrantClient(url=settings.qdrant_url)
