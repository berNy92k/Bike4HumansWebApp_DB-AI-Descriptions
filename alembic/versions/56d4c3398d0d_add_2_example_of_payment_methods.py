"""add 2 example of payment methods

Revision ID: 56d4c3398d0d
Revises: 40dad44922bb
Create Date: 2026-03-28 01:28:54.573891

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56d4c3398d0d'
down_revision: Union[str, Sequence[str], None] = '40dad44922bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    payment_methods_table = sa.table(
        "payment_methods",
        sa.column("name", sa.String),
        sa.column("price", sa.Float),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )

    now = datetime.utcnow()
    default_pm = [
        {
            "name": "Happy Path",
            "price": 2.5,
            "created_at": now,
            "updated_at": now
        },
        {
            "name": "Not Happy Path",
            "price": 5.42,
            "created_at": now,
            "updated_at": now
        }
    ]

    op.bulk_insert(payment_methods_table, default_pm)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("DELETE FROM payment_methods WHERE name IN ('Happy Path', 'Not Happy Path')"))
