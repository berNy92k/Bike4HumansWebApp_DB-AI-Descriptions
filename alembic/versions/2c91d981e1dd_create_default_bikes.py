"""create default bikes

Revision ID: 2c91d981e1dd
Revises: f5b1b8a7af5e
Create Date: 2026-03-23 00:57:08.581250

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c91d981e1dd'
down_revision: Union[str, Sequence[str], None] = 'f5b1b8a7af5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    biznes_user_id = conn.execute(
        sa.text("SELECT id FROM user WHERE username = :username"),
        {"username": "biznes"},
    ).scalar_one()

    trek_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Trek"},
    ).scalar_one()

    scott_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Scott"},
    ).scalar_one()

    klein_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Klein"},
    ).scalar_one()

    olympia_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Olympia"},
    ).scalar_one()

    bike_table = sa.table(
        "bikes",
        sa.Column("name", sa.String),
        sa.Column("description", sa.Text),
        sa.Column("price", sa.Numeric),
        sa.Column("stock_quantity", sa.Integer),
        sa.Column("image_url", sa.String),
        sa.Column("is_active", sa.Boolean),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("created_by", sa.Integer),
        sa.Column("brand_id", sa.Integer),
    )

    now = datetime.utcnow()
    default_bikes = [
        {
            "name": "Trek Marlin 7",
            "description": "Uniwersalny rower górski do codziennej jazdy i weekendowych tras.",
            "price": 4299.00,
            "stock_quantity": 5,
            "image_url": "/static/images/bikes/placeholders/bike1.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": trek_brand_id,
        },
        {
            "name": "Scott Scale 970",
            "description": "Lekki hardtail do szybkiej jazdy w terenie.",
            "price": 5899.00,
            "stock_quantity": 3,
            "image_url": "/static/images/bikes/placeholders/bike2.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": scott_brand_id,
        },
        {
            "name": "Klein Attitude",
            "description": "Klasyczny model MTB z naciskiem na wygodę i trwałość.",
            "price": 3499.00,
            "stock_quantity": 4,
            "image_url": "/static/images/bikes/placeholders/bike3.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": klein_brand_id,
        },
        {
            "name": "Olympia City Line",
            "description": "Miejski rower do codziennych dojazdów i rekreacyjnych przejażdżek.",
            "price": 2599.00,
            "stock_quantity": 8,
            "image_url": "/static/images/bikes/placeholders/bike4.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": olympia_brand_id,
        },
        {
            "name": "Trek FX 3",
            "description": "Lekki fitness bike do asfaltu, ścieżek rowerowych i dłuższych tras.",
            "price": 3799.00,
            "stock_quantity": 6,
            "image_url": "/static/images/bikes/placeholders/bike.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": trek_brand_id,
        },
    ]

    op.bulk_insert(bike_table, default_bikes)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "DELETE FROM bikes WHERE name IN "
            "('Trek Marlin 7', 'Scott Scale 970', 'Klein Attitude', "
            "'Olympia City Line', 'Trek FX 3')"
        )
    )
