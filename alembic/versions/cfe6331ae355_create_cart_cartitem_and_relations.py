"""create cart cartItem and relations

Revision ID: cfe6331ae355
Revises: 096afa6e554a
Create Date: 2026-03-27 21:09:42.980445

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfe6331ae355'
down_revision: Union[str, Sequence[str], None] = '096afa6e554a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cart_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cart_id", sa.Integer(), nullable=False),
        sa.Column("bike_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["cart_id"], ["carts.id"]),
        sa.ForeignKeyConstraint(["bike_id"], ["bikes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cart_items_id"), "cart_items", ["id"], unique=True)
    op.create_index(op.f("ix_cart_items_cart_id"), "cart_items", ["cart_id"], unique=False)
    op.create_index(op.f("ix_cart_items_bike_id"), "cart_items", ["bike_id"], unique=False)

    op.create_table(
        "carts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_carts_id"), "carts", ["id"], unique=True)
    op.create_index(op.f("ix_carts_user_id"), "carts", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cart_items_bike_id"), table_name="cart_items")
    op.drop_index(op.f("ix_cart_items_cart_id"), table_name="cart_items")
    op.drop_index(op.f("ix_cart_items_id"), table_name="cart_items")
    op.drop_table("cart_items")

    op.drop_index(op.f("ix_carts_user_id"), table_name="carts")
    op.drop_index(op.f("ix_carts_id"), table_name="carts")
    op.drop_table("carts")