"""seed manufacturer catalog expansion (phase 1 of bigger catalog)

Revision ID: b5c380dddcc4
Revises: b8f2c6a1d9e7
Create Date: 2026-07-27 12:00:00.000000

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b5c380dddcc4"
down_revision: Union[str, Sequence[str], None] = "b8f2c6a1d9e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 25 additional real-world bike manufacturer names, extending the existing
# Trek/Scott/Klein/Olympia/Giant/KTM/Felt/Devinci/Yuba/Corratec set as part of
# a larger catalog expansion (see the paired bike-seed migration that follows).
# Logo images are generated placeholder badges (app/static/images/manufacturers/placeholders/),
# not scraped brand logos, to avoid any trademark concerns.
NEW_MANUFACTURERS = [
    {'name': 'Cannondale',
 'slug': 'cannondale',
 'description': 'Amerykański producent rowerów górskich i szosowych, znany z innowacyjnych '
                'aluminiowych ram i technologii amortyzacji Lefty.',
 'is_ai': True},
    {'name': 'Specialized',
 'slug': 'specialized',
 'description': 'Duża amerykańska marka, mają chyba wszystko - górskie, szosowe, elektryki.',
 'is_ai': False},
    {'name': 'Merida',
 'slug': 'merida',
 'description': 'Tajwański producent oferujący szeroką gamę rowerów górskich, szosowych i '
                'miejskich w przystępnych cenach.',
 'is_ai': True},
    {'name': 'Cube',
 'slug': 'cube',
 'description': 'Niemiecka firma, dobry stosunek jakości do ceny, sporo elektryków w ofercie.',
 'is_ai': False},
    {'name': 'Canyon',
 'slug': 'canyon',
 'description': 'Niemiecka marka sprzedająca rowery bezpośrednio online, ceniona za lekkie ramy '
                'szosowe i gravelowe.',
 'is_ai': True},
    {'name': 'Orbea',
 'slug': 'orbea',
 'description': 'Hiszpańska marka z długą historią, rowery górskie i szosowe.',
 'is_ai': False},
    {'name': 'BMC',
 'slug': 'bmc',
 'description': 'Szwajcarski producent rowerów wyścigowych, obecny w peletonie najważniejszych '
                'wyścigów szosowych.',
 'is_ai': True},
    {'name': 'Bianchi',
 'slug': 'bianchi',
 'description': 'Włoski producent, charakterystyczny kolor celeste, głównie rowery szosowe.',
 'is_ai': False},
    {'name': 'Cervelo',
 'slug': 'cervelo',
 'description': 'Kanadyjska marka specjalizująca się w aerodynamicznych ramach szosowych i '
                'triathlonowych.',
 'is_ai': True},
    {'name': 'Santa Cruz',
 'slug': 'santa_cruz',
 'description': 'Amerykańska firma, mocne rowery górskie, głównie do enduro i downhille.',
 'is_ai': False},
    {'name': 'Kona',
 'slug': 'kona',
 'description': 'Kanadyjski producent oferujący rowery górskie, gravelowe oraz BMX o wyrazistym '
                'charakterze.',
 'is_ai': True},
    {'name': 'Ghost',
 'slug': 'ghost',
 'description': 'Niemiecka marka, sporo modeli górskich i elektrycznych, niezła jakość jak za te '
                'pieniądze.',
 'is_ai': False},
    {'name': 'Focus',
 'slug': 'focus',
 'description': 'Niemiecki producent rowerów szosowych i elektrycznych, znany z zaawansowanych ram '
                'karbonowych.',
 'is_ai': True},
    {'name': 'Riese & Muller',
 'slug': 'riese_muller',
 'description': "Niemiecka firma od e-bike'ów premium, drogie ale porządnie zrobione.",
 'is_ai': False},
    {'name': 'Pinarello',
 'slug': 'pinarello',
 'description': 'Włoska marka premium rowerów szosowych, wybierana przez zawodowców startujących w '
                'wielkich tourach.',
 'is_ai': True},
    {'name': 'Rocky Mountain',
 'slug': 'rocky_mountain',
 'description': 'Kanadyjska firma, rowery górskie, popularne wśród ludzi jeżdżących w terenie.',
 'is_ai': False},
    {'name': 'Marin',
 'slug': 'marin',
 'description': 'Amerykański producent rowerów górskich i gravelowych, jeden z pionierów mountain '
                "bike'u z Kalifornii.",
 'is_ai': True},
    {'name': 'Diamondback',
 'slug': 'diamondback',
 'description': 'Amerykańska marka, sporo tańszych rowerów górskich i BMX.',
 'is_ai': False},
    {'name': 'Raleigh',
 'slug': 'raleigh',
 'description': 'Brytyjska marka o wieloletniej tradycji, oferująca rowery miejskie, trekkingowe i '
                'szosowe.',
 'is_ai': True},
    {'name': 'Schwinn',
 'slug': 'schwinn',
 'description': 'Znana amerykańska marka, rowery miejskie i dziecięce, klasyka.',
 'is_ai': False},
    {'name': 'Woom',
 'slug': 'woom',
 'description': 'Austriacki producent rowerów dziecięcych projektowanych od podstaw z myślą o '
                'najmłodszych - lekkie ramy i dopasowana geometria.',
 'is_ai': True},
    {'name': 'Puky',
 'slug': 'puky',
 'description': 'Niemiecka firma od rowerków dla dzieci, popularna, sprawdzona marka.',
 'is_ai': False},
    {'name': 'GT Bicycles',
 'slug': 'gt_bicycles',
 'description': 'Amerykańska marka z bogatą historią w BMX i rowerach górskich.',
 'is_ai': True},
    {'name': 'Mongoose',
 'slug': 'mongoose',
 'description': 'Znana marka BMX i rowerów górskich, często wybierana przez młodszych rowerzystów.',
 'is_ai': False},
    {'name': 'Haro',
 'slug': 'haro',
 'description': 'Marka BMX założona przez byłego zawodnika, kultowa wśród fanów tej dyscypliny.',
 'is_ai': False},
]


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    biznes_user_id = conn.execute(
        sa.text("SELECT id FROM user WHERE username = :username"),
        {"username": "biznes"},
    ).scalar_one()

    manufacturer_table = sa.table(
        "manufacturer",
        sa.Column("name", sa.String),
        sa.Column("description", sa.Text),
        sa.Column("is_description_ai_generated", sa.Boolean),
        sa.Column("image_url", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("created_by", sa.Integer),
    )

    now = datetime.utcnow()
    rows = [
        {
            "name": m["name"],
            "description": m["description"],
            "is_description_ai_generated": m["is_ai"],
            "image_url": f"/static/images/manufacturers/placeholders/{m['slug']}.png",
            "created_at": now,
            "updated_at": now,
            "created_by": biznes_user_id,
        }
        for m in NEW_MANUFACTURERS
    ]

    op.bulk_insert(manufacturer_table, rows)


def downgrade() -> None:
    """Downgrade schema."""
    names = [m["name"] for m in NEW_MANUFACTURERS]
    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM manufacturer WHERE name IN :names").bindparams(
            sa.bindparam("names", expanding=True)
        ),
        {"names": names},
    )
