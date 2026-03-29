"""create order_id for new orders

Revision ID: 3a8e5ac07645
Revises: de2caf3b3b3b
Create Date: 2026-03-29 00:17:52.830211

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a8e5ac07645'
down_revision: Union[str, Sequence[str], None] = 'de2caf3b3b3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    """Upgrade schema."""
    with op.batch_alter_table("orders") as batch_op:
        batch_op.add_column(sa.Column("order_id", sa.String(length=11), nullable=True))
        batch_op.create_index(batch_op.f("ix_orders_order_id"), ["order_id"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("orders") as batch_op:
        batch_op.drop_index(batch_op.f("ix_orders_order_id"))
        batch_op.drop_column("order_id")
