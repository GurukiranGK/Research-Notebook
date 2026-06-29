from langchain_core.documents import Document
from qdrant_client.models import FieldCondition, Filter, MatchValue

from src.integrations.vectorstore import get_vectorstore


def search_chunks(
    *,
    document_id: str,
    user_id: str,
    query: str,
    limit: int = 5,
) -> list[Document]:
    vectorstore = get_vectorstore()

    qdrant_filter = Filter(
        must=[
            FieldCondition(
                key="metadata.documentId",
                match=MatchValue(value=document_id),
            ),
            FieldCondition(
                key="metadata.userId",
                match=MatchValue(value=user_id),
            ),
        ]
    )

    return vectorstore.similarity_search(
        query=query,
        k=limit,
        filter=qdrant_filter,
    )