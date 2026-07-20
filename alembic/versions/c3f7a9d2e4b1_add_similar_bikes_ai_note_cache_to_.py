"""add similar bikes AI note cache to bikes

Revision ID: c3f7a9d2e4b1
Revises: a1c4e6f2b9d3
Create Date: 2026-07-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3f7a9d2e4b1'
down_revision: Union[str, Sequence[str], None] = 'a1c4e6f2b9d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("bikes") as batch_op:
        batch_op.add_column(sa.Column("similar_bikes_ai_note", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("similar_bikes_ai_note_generated_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("bikes") as batch_op:
        batch_op.drop_column("similar_bikes_ai_note_generated_at")
        batch_op.drop_column("similar_bikes_ai_note")
