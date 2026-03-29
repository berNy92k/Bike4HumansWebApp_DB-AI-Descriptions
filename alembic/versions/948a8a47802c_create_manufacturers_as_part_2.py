"""create manufacturers as part 2

Revision ID: 948a8a47802c
Revises: 2c91d981e1dd
Create Date: 2026-03-23 19:50:26.548140

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '948a8a47802c'
down_revision: Union[str, Sequence[str], None] = '2c91d981e1dd'
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
            "name": "Giant",
            "description": "Przykładowy producent rowerów Giant.",
            "image_url": "/static/images/manufacturers/placeholders/giant.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
        {
            "name": "KTM",
            "description": "Przykładowy producent rowerów KTM.",
            "image_url": "/static/images/manufacturers/placeholders/ktm.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
        {
            "name": "Felt",
            "description": "Przykładowy producent rowerów Felt.",
            "image_url": "/static/images/manufacturers/placeholders/felt.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
        {
            "name": "Devinci",
            "description": "Przykładowy producent rowerów Devinci.",
            "image_url": "/static/images/manufacturers/placeholders/devinci.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
        {
            "name": "Yuba",
            "description": "Przykładowy producent rowerów Yuba.",
            "image_url": "/static/images/manufacturers/placeholders/yuba.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        },
        {
            "name": "Corratec",
            "description": "Przykładowy producent rowerów Corratec.",
            "image_url": "/static/images/manufacturers/placeholders/corratec.png",
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
            "DELETE FROM manufacturer WHERE name IN ('Giant', 'KTM', 'Felt', 'Devinci', 'Yuba', 'Corratec')"
        )
    )
