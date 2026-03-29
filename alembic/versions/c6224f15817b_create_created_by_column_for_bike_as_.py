"""create created_by column for bike as foreign_key

Revision ID: c6224f15817b
Revises: d238266aa8bb
Create Date: 2026-03-22 22:07:07.441918

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c6224f15817b'
down_revision: Union[str, Sequence[str], None] = 'd238266aa8bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("bikes") as batch_op:
        batch_op.add_column(
            sa.Column("created_by", sa.Integer(), nullable=False)
        )
        batch_op.create_foreign_key(
            "fk_bike_created_by_user",
            "user",
            ["created_by"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("bikes") as batch_op:
        batch_op.drop_constraint(
            "fk_bike_created_by_user",
            type_="foreignkey",
        )
        batch_op.drop_column("created_by")

# def upgrade() -> None:
#     """Upgrade schema."""
#     op.add_column(
#         "bikes",
#         sa.Column("created_by", sa.Integer, sa.ForeignKey("user.id"), nullable=False)
#     )
#
#
# def downgrade() -> None:
#     """Downgrade schema."""
#     op.drop_column("bikes", "created_by")
