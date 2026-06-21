from qdrant_client.models import Distance, FieldCondition, Filter, MatchValue, VectorParams

from src.core.config import get_settings
from src.integrations.qdrant import get_qdrant


def ensure_collection() -> None:
    settings = get_settings()
    qdrant = get_qdrant()
    collections = qdrant.get_collections()
    exists = any(collection.name == settings.qdrant_collection for collection in collections.collections)

    if not exists:
        qdrant.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )
        print("Qdrant collection created:", settings.qdrant_collection)
    else:
        print("Qdrant collection already exists")


def delete_document_vectors(*, document_id: str, user_id: str) -> None:
    settings = get_settings()
    qdrant = get_qdrant()
    collections = qdrant.get_collections()
    exists = any(collection.name == settings.qdrant_collection for collection in collections.collections)

    if not exists:
        return

    qdrant.delete(
        collection_name=settings.qdrant_collection,
        points_selector=Filter(
            must=[
                FieldCondition(key="documentId", match=MatchValue(value=document_id)),
                FieldCondition(key="userId", match=MatchValue(value=user_id)),
            ]
        ),
        wait=True,
    )
