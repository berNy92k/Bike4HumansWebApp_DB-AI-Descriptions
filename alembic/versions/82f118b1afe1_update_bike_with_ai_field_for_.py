"""update bike with AI field for description

Revision ID: 82f118b1afe1
Revises: d427c003fc67
Create Date: 2026-03-30 18:00:31.099859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82f118b1afe1'
down_revision: Union[str, Sequence[str], None] = 'd427c003fc67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("bikes") as batch_op:
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
    with op.batch_alter_table("bikes") as batch_op:
        batch_op.drop_column("is_description_ai_generated")
