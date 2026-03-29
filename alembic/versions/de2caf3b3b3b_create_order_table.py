"""create order table

Revision ID: de2caf3b3b3b
Revises: 56d4c3398d0d
Create Date: 2026-03-28 19:17:30.477242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de2caf3b3b3b'
down_revision: Union[str, Sequence[str], None] = '56d4c3398d0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("type", sa.String(), nullable=False, server_default="shipping"),
        sa.Column("company_name", sa.String(), nullable=True),
        sa.Column("vat_number", sa.String(), nullable=True),
        sa.Column("address_line_1", sa.String(), nullable=False),
        sa.Column("address_line_2", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("postal_code", sa.String(), nullable=False),
        sa.Column("country_code", sa.String(), nullable=False),
        sa.Column("state_province", sa.String(), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id"), nullable=False, index=True),
        sa.Column("currency", sa.String(), nullable=False, server_default="PLN"),
        sa.Column("status", sa.String(), nullable=False, server_default="PENDING"),
        sa.Column("total_price", sa.Float(), nullable=False, server_default="0"),
        sa.Column("payment_method_id", sa.Integer(), sa.ForeignKey("payment_methods.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False, index=True),
        sa.Column("bike_id", sa.Integer(), sa.ForeignKey("bikes.id"), nullable=False, index=True),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    with op.batch_alter_table("user") as batch_op:
        batch_op.add_column(sa.Column("address_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_user_address_id_addresses",
            "addresses",
            ["address_id"],
            ["id"],
        )


def downgrade() -> None:
    with op.batch_alter_table("user") as batch_op:
        batch_op.drop_constraint("fk_user_address_id_addresses", type_="foreignkey")
        batch_op.drop_column("address_id")

    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("addresses")
