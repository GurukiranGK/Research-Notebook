"""add conversations and messages

Revision ID: b455e18a40ac
Revises: 0001_initial
Create Date: 2026-06-24 22:47:41.077651
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b455e18a40ac"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "Conversation",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("userId", sa.String(), nullable=False),
        sa.Column("notebookId", sa.String(), nullable=False),
        sa.Column(
            "title",
            sa.String(),
            nullable=False,
            server_default="New conversation",
        ),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column(
            "createdAt",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updatedAt",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["userId"],
            ["User.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["notebookId"],
            ["Notebook.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "Conversation_userId_idx",
        "Conversation",
        ["userId"],
        unique=False,
    )
    op.create_index(
        "Conversation_notebookId_idx",
        "Conversation",
        ["notebookId"],
        unique=False,
    )

    op.create_table(
        "Message",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("conversationId", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "createdAt",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["conversationId"],
            ["Conversation.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "Message_conversationId_idx",
        "Message",
        ["conversationId"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "Message_conversationId_idx",
        table_name="Message",
    )
    op.drop_table("Message")

    op.drop_index(
        "Conversation_notebookId_idx",
        table_name="Conversation",
    )
    op.drop_index(
        "Conversation_userId_idx",
        table_name="Conversation",
    )
    op.drop_table("Conversation")