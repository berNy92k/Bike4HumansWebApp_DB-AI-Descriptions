"""add address id to checkouts and orders

Revision ID: f77c22ee0f0f
Revises: f1a68c92d347
Create Date: 2026-07-28 01:13:02.766989

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f77c22ee0f0f'
down_revision: Union[str, Sequence[str], None] = 'f1a68c92d347'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("checkouts") as batch_op:
        batch_op.add_column(sa.Column("address_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_checkouts_address_id_addresses", "addresses", ["address_id"], ["id"])

    with op.batch_alter_table("orders") as batch_op:
        batch_op.add_column(sa.Column("address_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_orders_address_id_addresses", "addresses", ["address_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("orders") as batch_op:
        batch_op.drop_constraint("fk_orders_address_id_addresses", type_="foreignkey")
        batch_op.drop_column("address_id")

    with op.batch_alter_table("checkouts") as batch_op:
        batch_op.drop_constraint("fk_checkouts_address_id_addresses", type_="foreignkey")
        batch_op.drop_column("address_id")
