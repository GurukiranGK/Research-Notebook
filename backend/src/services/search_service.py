from qdrant_client.models import FieldCondition, Filter, MatchValue

from src.core.config import get_settings
from src.integrations.gemini import get_embeddings
from src.integrations.qdrant import get_qdrant


def search_chunks(*, document_id: str, user_id: str, query: str, limit: int = 5):
    settings = get_settings()
    vector = get_embeddings().embed_query(query)

    return get_qdrant().search(
        collection_name=settings.qdrant_collection,
        query_vector=vector,
        limit=limit,
        query_filter=Filter(
            must=[
                FieldCondition(key="documentId", match=MatchValue(value=document_id)),
                FieldCondition(key="userId", match=MatchValue(value=user_id)),
            ]
        ),
    )
