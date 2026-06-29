from langchain_core.documents import Document

from src.db.models import Chunk
from src.integrations.vectorstore import get_vectorstore
from .vector_service import ensure_collection


def index_chunks(*, chunks: list[Chunk]) -> None:
    if not chunks:
        return

    ensure_collection()

    documents = [
        Document(
            page_content=chunk.content,
            metadata={
                "chunkId": chunk.id,
                "documentId": chunk.documentId,
                "userId": chunk.userId,
                "order": chunk.order,
            },
        )
        for chunk in chunks
    ]

    ids = [chunk.id for chunk in chunks]

    get_vectorstore().add_documents(
        documents=documents,
        ids=ids,
    )