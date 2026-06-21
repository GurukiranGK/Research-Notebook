from qdrant_client.models import PointStruct

from src.core.config import get_settings
from src.db.models import Chunk
from src.integrations.gemini import get_embeddings
from src.integrations.qdrant import get_qdrant
from .vector_service import ensure_collection


def index_chunks(*, chunks: list[Chunk]) -> None:
    if not chunks:
        return

    settings = get_settings()
    ensure_collection()

    vectors = get_embeddings().embed_documents([chunk.content for chunk in chunks])
    print("Embedding length:", len(vectors[0]) if vectors else None)

    points = [
        PointStruct(
            id=chunk.id,
            vector=vectors[index],
            payload={
                "documentId": chunk.documentId,
                "userId": chunk.userId,
                "order": chunk.order,
            },
        )
        for index, chunk in enumerate(chunks)
    ]

    get_qdrant().upsert(collection_name=settings.qdrant_collection, points=points)
