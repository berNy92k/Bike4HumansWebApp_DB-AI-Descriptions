"""create additional customer users

Revision ID: c2d7e9a41f68
Revises: 3a971e4de1f5
Create Date: 2026-07-27 13:00:00.000000

"""
from datetime import datetime
from typing import Sequence, Union
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c2d7e9a41f68"
down_revision: Union[str, Sequence[str], None] = "3a971e4de1f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# 16 fictional customer accounts, spreading the order history seeded in the
# following migration across more than the 3 pre-existing customer users.
# Password for each equals its username, matching the existing dev-seed convention.
NEW_CUSTOMERS = [
    ("anna.kowalska", "Anna", "Kowalska"),
    ("piotr.nowak", "Piotr", "Nowak"),
    ("katarzyna.wisniewska", "Katarzyna", "Wisniewska"),
    ("tomasz.wojcik", "Tomasz", "Wojcik"),
    ("magdalena.kowalczyk", "Magdalena", "Kowalczyk"),
    ("marek.kaminski", "Marek", "Kaminski"),
    ("agnieszka.lewandowska", "Agnieszka", "Lewandowska"),
    ("krzysztof.zielinski", "Krzysztof", "Zielinski"),
    ("ewa.szymanska", "Ewa", "Szymanska"),
    ("michal.wozniak", "Michal", "Wozniak"),
    ("joanna.dabrowska", "Joanna", "Dabrowska"),
    ("pawel.kozlowski", "Pawel", "Kozlowski"),
    ("natalia.jankowska", "Natalia", "Jankowska"),
    ("adam.mazur", "Adam", "Mazur"),
    ("karolina.kwiatkowska", "Karolina", "Kwiatkowska"),
    ("grzegorz.wojciechowski", "Grzegorz", "Wojciechowski"),
]


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    user_role_id = conn.execute(
        sa.text("SELECT id FROM role WHERE name = :name"),
        {"name": "user"},
    ).scalar_one()

    user_table = sa.table(
        "user",
        sa.Column("username", sa.String),
        sa.Column("email", sa.String),
        sa.Column("name", sa.String),
        sa.Column("surname", sa.String),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean),
        sa.Column("email_verified", sa.Boolean),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("role_id", sa.Integer),
    )

    now = datetime.utcnow()
    rows = [
        {
            "username": username,
            "email": f"{username}@example.com",
            "name": first_name,
            "surname": last_name,
            "hashed_password": crypt_context.hash(username),  # test only
            "is_active": True,
            "email_verified": True,
            "created_at": now,
            "updated_at": now,
            "role_id": user_role_id,
        }
        for username, first_name, last_name in NEW_CUSTOMERS
    ]

    op.bulk_insert(user_table, rows)


def downgrade() -> None:
    """Downgrade schema."""
    usernames = [u[0] for u in NEW_CUSTOMERS]
    conn = op.get_bind()
    conn.execute(
        sa.text("DELETE FROM user WHERE username IN :usernames").bindparams(
            sa.bindparam("usernames", expanding=True)
        ),
        {"usernames": usernames},
    )
