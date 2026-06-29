from langchain_qdrant import QdrantVectorStore

from src.core.config import get_settings
from src.integrations.gemini import get_embeddings
from src.integrations.qdrant import get_qdrant


def get_vectorstore() -> QdrantVectorStore:
    settings = get_settings()

    return QdrantVectorStore(
        client=get_qdrant(),
        collection_name=settings.qdrant_collection,
        embedding=get_embeddings(),
    )