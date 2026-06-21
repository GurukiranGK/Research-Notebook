from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from src.db.models import Chunk


class ChunkRepository:
    def delete_by_document(self, db: Session, *, document_id: str, user_id: str) -> int:
        result = db.execute(delete(Chunk).where(Chunk.documentId == document_id, Chunk.userId == user_id))
        db.commit()
        return result.rowcount or 0

    def bulk_create(self, db: Session, *, document_id: str, user_id: str, chunks: list[dict]) -> None:
        db.add_all(
            [
                Chunk(
                    documentId=document_id,
                    userId=user_id,
                    content=chunk["content"],
                    order=chunk["order"],
                )
                for chunk in chunks
            ]
        )
        db.commit()

    def find_by_document(self, db: Session, *, document_id: str, user_id: str) -> list[Chunk]:
        return list(
            db.scalars(
                select(Chunk)
                .where(Chunk.documentId == document_id, Chunk.userId == user_id)
                .order_by(Chunk.order.asc())
            )
        )

    def find_by_ids(
        self,
        db: Session,
        *,
        ids: list[str],
        user_id: str,
        document_id: str | None = None,
    ) -> list[Chunk]:
        if not ids:
            return []
        conditions = [Chunk.id.in_(ids), Chunk.userId == user_id]
        if document_id:
            conditions.append(Chunk.documentId == document_id)
        return list(
            db.scalars(
                select(Chunk)
                .where(*conditions)
                .order_by(Chunk.order.asc())
            )
        )
