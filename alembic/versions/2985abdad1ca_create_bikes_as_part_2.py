"""create bikes as part 2

Revision ID: 2985abdad1ca
Revises: 948a8a47802c
Create Date: 2026-03-23 19:56:33.234360

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2985abdad1ca'
down_revision: Union[str, Sequence[str], None] = '948a8a47802c'
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

    giant_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Giant"},
    ).scalar_one()

    ktm_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "KTM"},
    ).scalar_one()

    felt_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Felt"},
    ).scalar_one()

    devinci_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Devinci"},
    ).scalar_one()

    yuba_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Yuba"},
    ).scalar_one()

    corratec_brand_id = conn.execute(
        sa.text("SELECT id FROM manufacturer WHERE name = :name"),
        {"name": "Corratec"},
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
            "name": "Giant Talon 1",
            "description": "Uniwersalny hardtail do codziennej jazdy i lekkiego terenu.",
            "price": 4699.00,
            "stock_quantity": 4,
            "image_url": "/static/images/bikes/placeholders/bike5.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": giant_brand_id,
        },
        {
            "name": "KTM Ultra 1964",
            "description": "Sportowy rower MTB stworzony do dynamicznej jazdy.",
            "price": 6399.00,
            "stock_quantity": 3,
            "image_url": "/static/images/bikes/placeholders/bike6.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": ktm_brand_id,
        },
        {
            "name": "Felt Verza Speed 50",
            "description": "Lekki rower fitness do miasta, asfaltu i dłuższych tras.",
            "price": 3999.00,
            "stock_quantity": 5,
            "image_url": "/static/images/bikes/placeholders/bike7.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": felt_brand_id,
        },
        {
            "name": "Devinci Marshall",
            "description": "Nowoczesny rower trailowy do pewnej jazdy w trudniejszym terenie.",
            "price": 7899.00,
            "stock_quantity": 2,
            "image_url": "/static/images/bikes/placeholders/bike8.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": devinci_brand_id,
        },
        {
            "name": "Yuba Kombi",
            "description": "Praktyczny rower cargo do codziennych zadań i transportu.",
            "price": 8299.00,
            "stock_quantity": 2,
            "image_url": "/static/images/bikes/placeholders/bike9.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": yuba_brand_id,
        },
        {
            "name": "Corratec E-Power X Vert",
            "description": "E-bike do komfortowej jazdy po mieście i poza nim.",
            "price": 10999.00,
            "stock_quantity": 2,
            "image_url": "/static/images/bikes/placeholders/bike10.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": corratec_brand_id,
        },
        {
            "name": "Trek Domane AL 2",
            "description": "Szosa endurance do wygodnych, dłuższych przejazdów.",
            "price": 5299.00,
            "stock_quantity": 4,
            "image_url": "/static/images/bikes/placeholders/bike11.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": trek_brand_id,
        },
        {
            "name": "Scott Sub Cross 30",
            "description": "Crossowy model do miasta, ścieżek i weekendowych wycieczek.",
            "price": 4399.00,
            "stock_quantity": 3,
            "image_url": "/static/images/bikes/placeholders/bike12.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": scott_brand_id,
        },
        {
            "name": "Klein Pulse",
            "description": "Lekki i wygodny rower do rekreacyjnej jazdy w terenie.",
            "price": 3799.00,
            "stock_quantity": 5,
            "image_url": "/static/images/bikes/placeholders/bike13.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": klein_brand_id,
        },
        {
            "name": "Olympia Voyager",
            "description": "Miejski rower do codziennego użytkowania i spokojnych tras.",
            "price": 3199.00,
            "stock_quantity": 6,
            "image_url": "/static/images/bikes/placeholders/bike14.png",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
            "brand_id": olympia_brand_id,
        },
    ]

    op.bulk_insert(bike_table, default_bikes)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "DELETE FROM bikes WHERE name IN "
            "('Giant Talon 1', 'KTM Ultra 1964', 'Felt Verza Speed 50', "
            "'Devinci Marshall', 'Yuba Kombi', 'Corratec E-Power X Vert', "
            "'Trek Domane AL 2', 'Scott Sub Cross 30', 'Klein Pulse', "
            "'Olympia Voyager')"
        )
    )
