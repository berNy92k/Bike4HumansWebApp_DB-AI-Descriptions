"""update bikes with random new values for new fields

Revision ID: 096afa6e554a
Revises: 496f82d13c44
Create Date: 2026-03-26 22:24:04.170766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '096afa6e554a'
down_revision: Union[str, Sequence[str], None] = '496f82d13c44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    updates = [
        (
            "Giant Talon 1",
            "Uniwersalny hardtail do codziennej jazdy i lekkiego terenu. Rama 17 cali, koła 29 cali i stonowany grafitowy kolor sprawiają, że to bardzo wszechstronny model do miasta i lasu.",
            17,
            29,
            "Graphite Grey",
        ),
        (
            "KTM Ultra 1964",
            "Sportowy rower MTB stworzony do dynamicznej jazdy. Aluminiowa rama 18 cali, koła 29 cali i czerwono-czarna stylistyka podkreślają jego terenowy charakter.",
            18,
            29,
            "Black/Red",
        ),
        (
            "Felt Verza Speed 50",
            "Lekki rower fitness do miasta, asfaltu i dłuższych tras. Rama 19 cali, koła 28 cali oraz srebrno-niebieskie wykończenie zapewniają elegancki, szybki wygląd.",
            19,
            28,
            "Silver Blue",
        ),
        (
            "Devinci Marshall",
            "Nowoczesny rower trailowy do pewnej jazdy w trudniejszym terenie. Rama 18 cali, koła 29 cali i matowy zielony kolor dobrze pasują do agresywnej sylwetki modelu.",
            18,
            29,
            "Matte Olive",
        ),
        (
            "Yuba Kombi",
            "Praktyczny rower cargo do codziennych zadań i transportu. Stabilna rama 20 cali, koła 24 cali i żółte akcenty podkreślają użytkowy, miejski charakter.",
            20,
            24,
            "Utility Yellow",
        ),
        (
            "Corratec E-Power X Vert",
            "E-bike do komfortowej jazdy po mieście i poza nim. Rama 19 cali, koła 29 cali i grafitowo-szare wykończenie podkreślają nowoczesny, elektryczny charakter roweru.",
            19,
            29,
            "Graphite Grey",
        ),
        (
            "Trek Domane AL 2",
            "Szosa endurance do wygodnych, dłuższych przejazdów. Rama 52 cm, koła 28 cali i klasyczny niebieski kolor nadają mu elegancki, sportowy styl.",
            52,
            28,
            "Deep Blue",
        ),
        (
            "Scott Sub Cross 30",
            "Crossowy model do miasta, ścieżek i weekendowych wycieczek. Rama 18 cali, koła 28 cali oraz czarno-szare wykończenie gwarantują uniwersalny wygląd.",
            18,
            28,
            "Black Grey",
        ),
        (
            "Klein Pulse",
            "Lekki i wygodny rower do rekreacyjnej jazdy w terenie. Rama 17 cali, koła 27 cali i zielony lakier dobrze wpisują się w spokojny, terenowy styl.",
            17,
            27,
            "Forest Green",
        ),
        (
            "Olympia Voyager",
            "Miejski rower do codziennego użytkowania i spokojnych tras. Rama 19 cali, koła 28 cali i kremowo-niebieskie malowanie dodają mu klasy i lekkości.",
            19,
            28,
            "Cream Blue",
        ),
    ]

    for name, description, frame_size, wheel_size, color in updates:
        conn.execute(
            sa.text(
                """
                UPDATE bikes
                SET description = :description,
                    frame_size = :frame_size,
                    wheel_size = :wheel_size,
                    color = :color
                WHERE name = :name
                """
            ),
            {
                "name": name,
                "description": description,
                "frame_size": frame_size,
                "wheel_size": wheel_size,
                "color": color,
            },
        )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()

    for name in [
        "Giant Talon 1",
        "KTM Ultra 1964",
        "Felt Verza Speed 50",
        "Devinci Marshall",
        "Yuba Kombi",
        "Corratec E-Power X Vert",
        "Trek Domane AL 2",
        "Scott Sub Cross 30",
        "Klein Pulse",
        "Olympia Voyager",
    ]:
        conn.execute(
            sa.text(
                """
                UPDATE bikes
                SET description = NULL,
                    frame_size = NULL,
                    wheel_size = NULL,
                    color = NULL
                WHERE name = :name
                """
            ),
            {"name": name},
        )
