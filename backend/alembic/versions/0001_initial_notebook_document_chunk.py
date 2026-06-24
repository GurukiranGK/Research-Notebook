"""initial notebook document chunk schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-20
"""

from typing import Sequence, Union

from alembic import context, op
import sqlalchemy as sa


revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(inspector: sa.Inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def _index_exists(inspector: sa.Inspector, table_name: str, index_name: str) -> bool:
    return any(index["name"] == index_name for index in inspector.get_indexes(table_name))


def _foreign_key_exists(inspector: sa.Inspector, table_name: str, fk_name: str) -> bool:
    return any(fk["name"] == fk_name for fk in inspector.get_foreign_keys(table_name))


def _create_notebook_table() -> None:
    op.create_table(
        "Notebook",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("userId", sa.String(), nullable=False),
        sa.Column("createdAt", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updatedAt", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="Notebook_pkey"),
    )


def _create_document_table() -> None:
    op.create_table(
        "Document",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("notebookId", sa.String(), nullable=False),
        sa.Column("userId", sa.String(), nullable=False),
        sa.Column("filename", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("createdAt", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="Document_pkey"),
    )


def _create_chunk_table() -> None:
    op.create_table(
        "Chunk",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("documentId", sa.String(), nullable=False),
        sa.Column("userId", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("createdAt", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="Chunk_pkey"),
    )


def _create_indexes_and_foreign_keys() -> None:
    op.create_index("Notebook_userId_idx", "Notebook", ["userId"])
    op.create_index("Document_notebookId_idx", "Document", ["notebookId"])
    op.create_index("Document_userId_idx", "Document", ["userId"])
    op.create_foreign_key(
        "Document_notebookId_fkey",
        "Document",
        "Notebook",
        ["notebookId"],
        ["id"],
        onupdate="CASCADE",
        ondelete="RESTRICT",
    )
    op.create_index("Chunk_documentId_idx", "Chunk", ["documentId"])
    op.create_index("Chunk_userId_idx", "Chunk", ["userId"])
    op.create_foreign_key(
        "Chunk_documentId_fkey",
        "Chunk",
        "Document",
        ["documentId"],
        ["id"],
        onupdate="CASCADE",
        ondelete="RESTRICT",
    )


def _upgrade_offline() -> None:
    _create_notebook_table()
    _create_document_table()
    _create_chunk_table()
    _create_indexes_and_foreign_keys()


def _upgrade_online() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _table_exists(inspector, "Notebook"):
        _create_notebook_table()
        inspector = sa.inspect(bind)

    if not _index_exists(inspector, "Notebook", "Notebook_userId_idx"):
        op.create_index("Notebook_userId_idx", "Notebook", ["userId"])

    op.execute('ALTER TABLE "Notebook" ALTER COLUMN "updatedAt" SET DEFAULT CURRENT_TIMESTAMP')

    if not _table_exists(inspector, "Document"):
        _create_document_table()
        inspector = sa.inspect(bind)

    if not _index_exists(inspector, "Document", "Document_notebookId_idx"):
        op.create_index("Document_notebookId_idx", "Document", ["notebookId"])
    if not _index_exists(inspector, "Document", "Document_userId_idx"):
        op.create_index("Document_userId_idx", "Document", ["userId"])
    if not _foreign_key_exists(inspector, "Document", "Document_notebookId_fkey"):
        op.create_foreign_key(
            "Document_notebookId_fkey",
            "Document",
            "Notebook",
            ["notebookId"],
            ["id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        )

    if not _table_exists(inspector, "Chunk"):
        _create_chunk_table()
        inspector = sa.inspect(bind)

    if not _index_exists(inspector, "Chunk", "Chunk_documentId_idx"):
        op.create_index("Chunk_documentId_idx", "Chunk", ["documentId"])
    if not _index_exists(inspector, "Chunk", "Chunk_userId_idx"):
        op.create_index("Chunk_userId_idx", "Chunk", ["userId"])
    if not _foreign_key_exists(inspector, "Chunk", "Chunk_documentId_fkey"):
        op.create_foreign_key(
            "Chunk_documentId_fkey",
            "Chunk",
            "Document",
            ["documentId"],
            ["id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        )


def upgrade() -> None:
    if context.is_offline_mode():
        _upgrade_offline()
    else:
        _upgrade_online()


def downgrade() -> None:
    op.drop_constraint("Chunk_documentId_fkey", "Chunk", type_="foreignkey")
    op.drop_index("Chunk_userId_idx", table_name="Chunk")
    op.drop_index("Chunk_documentId_idx", table_name="Chunk")
    op.drop_table("Chunk")

    op.drop_constraint("Document_notebookId_fkey", "Document", type_="foreignkey")
    op.drop_index("Document_userId_idx", table_name="Document")
    op.drop_index("Document_notebookId_idx", table_name="Document")
    op.drop_table("Document")

    op.drop_index("Notebook_userId_idx", table_name="Notebook")
    op.drop_table("Notebook")

