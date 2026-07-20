"""update manufacturer with AI field for description

Revision ID: a1c4e6f2b9d3
Revises: 2ebdd9595d8d
Create Date: 2026-07-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c4e6f2b9d3'
down_revision: Union[str, Sequence[str], None] = '2ebdd9595d8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("manufacturer") as batch_op:
        batch_op.add_column(
            sa.Column(
                "is_description_ai_generated",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("manufacturer") as batch_op:
        batch_op.drop_column("is_description_ai_generated")
