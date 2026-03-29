"""create default users

Revision ID: 2182a218ff25
Revises: f80243bf47ea
Create Date: 2026-03-22 20:07:00.806940

"""
from datetime import datetime
from typing import Sequence, Union
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2182a218ff25'
down_revision: Union[str, Sequence[str], None] = 'f80243bf47ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    super_admin_role_id = conn.execute(
        sa.text("SELECT id FROM role WHERE name = :name"),
        {"name": "super_admin"}
    ).scalar_one()

    admin_role_id = conn.execute(
        sa.text("SELECT id FROM role WHERE name = :name"),
        {"name": "admin"}
    ).scalar_one()

    normal_role_id = conn.execute(
        sa.text("SELECT id FROM role WHERE name = :name"),
        {"name": "user"}
    ).scalar_one()

    biznes_role_id = conn.execute(
        sa.text("SELECT id FROM role WHERE name = :name"),
        {"name": "manager"}
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
        sa.Column("role_id", sa.Integer)
    )

    now = datetime.utcnow()
    default_users = [
        {
            "username":"superadmin",
            "email": "superadmin@bike4humans.pl",
            "name": "Super",
            "surname": "Admin",
            "hashed_password": crypt_context.hash("superadmin"), # test only
            "is_active": True,
            "email_verified": True,
            "created_at": now,
            "updated_at": now,
            "role_id": super_admin_role_id
        },
        {
            "username":"admin",
            "email": "admin@bike4humans.pl",
            "name": "Normal",
            "surname": "Admin",
            "hashed_password": crypt_context.hash("admin"), # test only
            "is_active": True,
            "email_verified": True,
            "created_at": now,
            "updated_at": now,
            "role_id": admin_role_id
        },
        {
            "username":"normal",
            "email": "normal@bike4humans.pl",
            "name": "Josef",
            "surname": "Opotkowski",
            "hashed_password": crypt_context.hash("normal"), # test only
            "is_active": True,
            "email_verified": True,
            "created_at": now,
            "updated_at": now,
            "role_id": normal_role_id
        },
        {
            "username":"biznes",
            "email": "biznes@bike4humans.pl",
            "name": "Biznes",
            "surname": "Dodawacze",
            "hashed_password": crypt_context.hash("biznes"), # test only
            "is_active": True,
            "email_verified": True,
            "created_at": now,
            "updated_at": now,
            "role_id": biznes_role_id
        }
    ]

    op.bulk_insert(user_table, default_users)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        sa.text(
            "DELETE FROM user WHERE username IN ('superadmin', 'admin', 'normal')"
        )
    )
