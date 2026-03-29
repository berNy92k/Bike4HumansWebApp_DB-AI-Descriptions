"""add payment method

Revision ID: 40dad44922bb
Revises: 557f60b62a00
Create Date: 2026-03-28 01:25:01.095954

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40dad44922bb'
down_revision: Union[str, Sequence[str], None] = '557f60b62a00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "payment_methods",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    with op.batch_alter_table("checkouts") as batch_op:
        batch_op.add_column(sa.Column("payment_method_id", sa.Integer(), nullable=True))

    op.execute("UPDATE checkouts SET payment_method_id = 1 WHERE payment_method_id IS NULL")

    with op.batch_alter_table("checkouts") as batch_op:
        batch_op.create_foreign_key(
            "fk_checkouts_payment_method_id_payment_methods",
            "payment_methods",
            ["payment_method_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("checkouts") as batch_op:
        batch_op.drop_constraint(
            "fk_checkouts_payment_method_id_payment_methods",
            type_="foreignkey",
        )
        batch_op.drop_column("payment_method_id")

    op.drop_table("payment_methods")
