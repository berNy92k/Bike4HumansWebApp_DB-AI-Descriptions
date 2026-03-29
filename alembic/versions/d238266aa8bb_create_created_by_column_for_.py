"""create created_by column for manufacturers as foreign_key

Revision ID: d238266aa8bb
Revises: 2182a218ff25
Create Date: 2026-03-22 21:43:07.965682

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd238266aa8bb'
down_revision: Union[str, Sequence[str], None] = '2182a218ff25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("manufacturer") as batch_op:
        batch_op.add_column(
            sa.Column("created_by", sa.Integer(), nullable=False)
        )
        batch_op.create_foreign_key(
            "fk_manufacturer_created_by_user",
            "user",
            ["created_by"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("manufacturer") as batch_op:
        batch_op.drop_constraint(
            "fk_manufacturer_created_by_user",
            type_="foreignkey",
        )
        batch_op.drop_column("created_by")

# def upgrade() -> None:
#     """Upgrade schema."""
#     op.add_column(
#         "manufacturer",
#         sa.Column("created_by", sa.Integer, sa.ForeignKey("user.id"), nullable=False)
#     )
#
#
# def downgrade() -> None:
#     """Downgrade schema."""
#     op.drop_column("manufacturer", "created_by")
