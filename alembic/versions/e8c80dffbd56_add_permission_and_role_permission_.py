"""add permission and role_permission tables

Revision ID: e8c80dffbd56
Revises: 82f118b1afe1
Create Date: 2026-07-16 02:19:01.100938

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8c80dffbd56'
down_revision: Union[str, Sequence[str], None] = '82f118b1afe1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ADMIN_PANEL_ACCESS = "ADMIN_PANEL_ACCESS"
SUPER_ADMIN = "SUPER_ADMIN"


def upgrade() -> None:
    """Upgrade schema."""
    now = datetime.utcnow()

    op.create_table(
        "permission",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_permission_code"), "permission", ["code"], unique=True)

    op.create_table(
        "role_permission",
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("role.id"), primary_key=True),
        sa.Column("permission_id", sa.Integer(), sa.ForeignKey("permission.id"), primary_key=True),
    )

    conn = op.get_bind()

    permission_table = sa.table(
        "permission",
        sa.column("id", sa.Integer),
        sa.column("code", sa.String),
        sa.column("description", sa.String),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
    )

    op.bulk_insert(
        permission_table,
        [
            {
                "code": ADMIN_PANEL_ACCESS,
                "description": "Dostęp do panelu admina (JSON API i strony renderowane).",
                "created_at": now,
                "updated_at": now,
            },
            {
                "code": SUPER_ADMIN,
                "description": "Zarządzanie rolami/uprawnieniami i nadawanie ról admin-owych innym userom.",
                "created_at": now,
                "updated_at": now,
            },
        ],
    )

    admin_panel_access_id = conn.execute(
        sa.text("SELECT id FROM permission WHERE code = :code"),
        {"code": ADMIN_PANEL_ACCESS},
    ).scalar_one()

    super_admin_permission_id = conn.execute(
        sa.text("SELECT id FROM permission WHERE code = :code"),
        {"code": SUPER_ADMIN},
    ).scalar_one()

    role_permission_table = sa.table(
        "role_permission",
        sa.column("role_id", sa.Integer),
        sa.column("permission_id", sa.Integer),
    )

    role_ids = {
        name: conn.execute(
            sa.text("SELECT id FROM role WHERE name = :name"),
            {"name": name},
        ).scalar_one()
        for name in ("super_admin", "admin", "manager", "user", "guest")
    }

    role_permission_rows = [
        {"role_id": role_ids["super_admin"], "permission_id": admin_panel_access_id},
        {"role_id": role_ids["super_admin"], "permission_id": super_admin_permission_id},
        {"role_id": role_ids["admin"], "permission_id": admin_panel_access_id},
        {"role_id": role_ids["manager"], "permission_id": admin_panel_access_id},
    ]

    op.bulk_insert(role_permission_table, role_permission_rows)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("role_permission")
    op.drop_index(op.f("ix_permission_code"), table_name="permission")
    op.drop_table("permission")
