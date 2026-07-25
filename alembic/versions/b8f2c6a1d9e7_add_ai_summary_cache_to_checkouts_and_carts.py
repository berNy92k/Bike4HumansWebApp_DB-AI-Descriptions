"""add AI summary cache to checkouts and carts

Revision ID: b8f2c6a1d9e7
Revises: d4e9b1c7a3f5
Create Date: 2026-07-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8f2c6a1d9e7'
down_revision: Union[str, Sequence[str], None] = 'd4e9b1c7a3f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("checkouts") as batch_op:
        batch_op.add_column(sa.Column("ai_summary", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("ai_summary_generated_at", sa.DateTime(), nullable=True))

    with op.batch_alter_table("carts") as batch_op:
        batch_op.add_column(sa.Column("ai_summary", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("ai_summary_generated_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("carts") as batch_op:
        batch_op.drop_column("ai_summary_generated_at")
        batch_op.drop_column("ai_summary")

    with op.batch_alter_table("checkouts") as batch_op:
        batch_op.drop_column("ai_summary_generated_at")
        batch_op.drop_column("ai_summary")
