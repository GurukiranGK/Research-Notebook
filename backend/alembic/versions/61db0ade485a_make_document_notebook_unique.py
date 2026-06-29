"""make document notebook unique

Revision ID: 61db0ade485a
Revises: b455e18a40ac
Create Date: 2026-06-28 16:22:44.277295
"""

from typing import Sequence, Union

from alembic import op


revision: str = "61db0ade485a"
down_revision: Union[str, None] = "b455e18a40ac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "Document_notebookId_unique",
        "Document",
        ["notebookId"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "Document_notebookId_unique",
        "Document",
        type_="unique",
    )