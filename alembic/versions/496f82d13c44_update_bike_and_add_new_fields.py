"""update bike and add new fields

Revision ID: 496f82d13c44
Revises: 2985abdad1ca
Create Date: 2026-03-26 22:20:22.296333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '496f82d13c44'
down_revision: Union[str, Sequence[str], None] = '2985abdad1ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('bikes', sa.Column('frame_size', sa.Integer(), nullable=True))
    op.add_column('bikes', sa.Column('wheel_size', sa.Integer(), nullable=True))
    op.add_column('bikes', sa.Column('color', sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('bikes', 'color')
    op.drop_column('bikes', 'wheel_size')
    op.drop_column('bikes', 'frame_size')
