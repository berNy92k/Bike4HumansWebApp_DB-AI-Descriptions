"""create new fields for bike

Revision ID: d58052c7b7be
Revises: 3a8e5ac07645
Create Date: 2026-03-30 17:05:36.370853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd58052c7b7be'
down_revision: Union[str, Sequence[str], None] = '3a8e5ac07645'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('bikes', sa.Column('bike_type', sa.String(length=100), nullable=True))
    op.add_column('bikes', sa.Column('frame_material', sa.String(length=100), nullable=True))
    op.add_column('bikes', sa.Column('frame_size_label', sa.String(length=20), nullable=True))
    op.add_column('bikes', sa.Column('tire_width', sa.Integer(), nullable=True))
    op.add_column('bikes', sa.Column('gear_count', sa.Integer(), nullable=True))
    op.add_column('bikes', sa.Column('brake_type', sa.String(length=100), nullable=True))
    op.add_column('bikes', sa.Column('suspension_type', sa.String(length=100), nullable=True))
    op.add_column('bikes', sa.Column('weight_kg', sa.Numeric(5, 2), nullable=True))
    op.add_column('bikes', sa.Column('recommended_height_min', sa.Integer(), nullable=True))
    op.add_column('bikes', sa.Column('recommended_height_max', sa.Integer(), nullable=True))
    op.add_column('bikes', sa.Column('usage', sa.String(length=100), nullable=True))
    op.add_column('bikes', sa.Column('target_user', sa.String(length=100), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('bikes', 'target_user')
    op.drop_column('bikes', 'usage')
    op.drop_column('bikes', 'recommended_height_max')
    op.drop_column('bikes', 'recommended_height_min')
    op.drop_column('bikes', 'weight_kg')
    op.drop_column('bikes', 'suspension_type')
    op.drop_column('bikes', 'brake_type')
    op.drop_column('bikes', 'gear_count')
    op.drop_column('bikes', 'tire_width')
    op.drop_column('bikes', 'frame_size_label')
    op.drop_column('bikes', 'frame_material')
    op.drop_column('bikes', 'bike_type')
