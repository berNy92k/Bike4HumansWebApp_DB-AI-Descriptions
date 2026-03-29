"""create brand_id column for bike as foreign_key, remove slug, brand and category

Revision ID: 5027c9788680
Revises: c6224f15817b
Create Date: 2026-03-22 23:24:51.109570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5027c9788680'
down_revision: Union[str, Sequence[str], None] = 'c6224f15817b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("bikes") as batch_op:
        batch_op.drop_index("ix_bikes_slug")
        batch_op.drop_index("ix_bikes_category")
        batch_op.drop_index("ix_bikes_brand")
        batch_op.drop_column("slug")
        batch_op.drop_column("brand")
        batch_op.drop_column("category")
        batch_op.add_column(sa.Column("brand_id", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("bikes") as batch_op:
        batch_op.drop_constraint(
            "fk_bikes_brand_id_manufacturers",
            type_="foreignkey",
        )
        batch_op.drop_column("brand_id")
        batch_op.add_column(sa.Column("slug", sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column("brand", sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column("category", sa.String(length=100), nullable=True))
        batch_op.create_index("ix_bikes_slug", 'slug', ["slug"], unique=False)
        batch_op.create_index("ix_bikes_brand", 'bikes', ['brand'], unique=False)
        batch_op.create_index("ix_bikes_category", 'bikes', ['category'], unique=False)