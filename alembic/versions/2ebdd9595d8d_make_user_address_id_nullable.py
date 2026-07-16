"""make user address_id nullable

Revision ID: 2ebdd9595d8d
Revises: e8c80dffbd56
Create Date: 2026-07-17 01:12:57.648713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ebdd9595d8d'
down_revision: Union[str, Sequence[str], None] = 'e8c80dffbd56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("user") as batch_op:
        batch_op.alter_column(
            "address_id",
            existing_type=sa.Integer(),
            nullable=True,
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("user") as batch_op:
        batch_op.alter_column(
            "address_id",
            existing_type=sa.Integer(),
            nullable=False,
        )
