"""create default manufacturers

Revision ID: f5b1b8a7af5e
Revises: 5027c9788680
Create Date: 2026-03-23 00:49:12.783855

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5b1b8a7af5e'
down_revision: Union[str, Sequence[str], None] = '5027c9788680'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    biznes_user_id = conn.execute(
        sa.text("SELECT id FROM user WHERE username = :username"),
        {"username": "biznes"}
    ).scalar_one()

    manufacturer_table = sa.table(
        "manufacturer",
        sa.Column("name", sa.String),
        sa.Column("description", sa.Text),
        sa.Column("image_url", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("created_by", sa.Integer),
    )

    now = datetime.utcnow()

    default_manufacturers = [
        {
            "name": "Trek",
            "description": "Przykładowy producent rowerów Trek.",
            "image_url": "/static/images/manufacturers/placeholders/trek.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
        {
            "name": "Scott",
            "description": "Przykładowy producent rowerów Scott.",
            "image_url": "/static/images/manufacturers/placeholders/scott.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
        {
            "name": "Klein",
            "description": "Przykładowy producent rowerów Klein.",
            "image_url": "/static/images/manufacturers/placeholders/klein.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
        {
            "name": "Olympia",
            "description": "Przykładowy producent rowerów Olympia.",
            "image_url": "/static/images/manufacturers/placeholders/olympia.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
    ]

    op.bulk_insert(manufacturer_table, default_manufacturers)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "DELETE FROM manufacturer WHERE name IN ('Trek', 'Scott', 'Klein', 'Olympia')"
        )
    )
