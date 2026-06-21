import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


def uuid_string() -> str:
    return str(uuid.uuid4())


class Notebook(Base):
    __tablename__ = "Notebook"
    __table_args__ = (Index("Notebook_userId_idx", "userId"),)

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_string)
    title: Mapped[str] = mapped_column(String, nullable=False)
    userId: Mapped[str] = mapped_column(String, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    documents: Mapped[list["Document"]] = relationship(
        back_populates="notebook", cascade="all, delete"
    )


class Document(Base):
    __tablename__ = "Document"
    __table_args__ = (
        Index("Document_notebookId_idx", "notebookId"),
        Index("Document_userId_idx", "userId"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_string)
    notebookId: Mapped[str] = mapped_column(String, ForeignKey("Notebook.id"), nullable=False)
    userId: Mapped[str] = mapped_column(String, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    notebook: Mapped[Notebook] = relationship(back_populates="documents")
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete")


class Chunk(Base):
    __tablename__ = "Chunk"
    __table_args__ = (
        Index("Chunk_documentId_idx", "documentId"),
        Index("Chunk_userId_idx", "userId"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_string)
    documentId: Mapped[str] = mapped_column(String, ForeignKey("Document.id"), nullable=False)
    userId: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    document: Mapped[Document] = relationship(back_populates="chunks")
