"""create default roles

Revision ID: f80243bf47ea
Revises: d5b81b10c732
Create Date: 2026-03-22 19:20:32.724526

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f80243bf47ea'
down_revision: Union[str, Sequence[str], None] = 'd5b81b10c732'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    role_table = sa.table(
        "role",
        sa.Column("name", sa.String),
        sa.Column("description", sa.String),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime)
    )

    now = datetime.utcnow()

    default_roles = [
        {"name": "super_admin", "description": "Super Admin serwisu. Może dokonywać każdą zmianę", "created_at": now, "updated_at": now},
        {"name": "admin", "description": "Admin serwisu. Może dokonywać większość zmian, oprócz dodawania użytkowników.", "created_at": now, "updated_at": now},
        {"name": "manager", "description": "Rola podobna do admina. Moze dodawac produkty.", "created_at": now, "updated_at": now},
        {"name": "user", "description": "Podstawowa rola dla nowo utworzonego użytkownika. Nie może edytować treści.", "created_at": now, "updated_at": now},
        {"name": "guest", "description": "Konto użytkownika stworzone w trakcie dokonywania zamówienia jako gość/ guest", "created_at": now, "updated_at": now},
    ]

    op.bulk_insert(role_table, default_roles)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "DELETE FROM role WHERE name IN ('super_admin', 'admin', 'user', 'guest')"
        )
    )
