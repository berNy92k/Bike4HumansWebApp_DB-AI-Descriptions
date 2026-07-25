"""add AI summary cache to orders

Revision ID: d4e9b1c7a3f5
Revises: c3f7a9d2e4b1
Create Date: 2026-07-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e9b1c7a3f5'
down_revision: Union[str, Sequence[str], None] = 'c3f7a9d2e4b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("orders") as batch_op:
        batch_op.add_column(sa.Column("ai_summary", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("ai_summary_generated_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("orders") as batch_op:
        batch_op.drop_column("ai_summary_generated_at")
        batch_op.drop_column("ai_summary")
