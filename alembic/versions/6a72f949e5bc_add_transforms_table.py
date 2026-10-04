"""add transforms table

Revision ID: 6a72f949e5bc
Revises: 3ec8b6ba896f
Create Date: 2026-10-04 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6a72f949e5bc'
down_revision: Union[str, Sequence[str], None] = '3ec8b6ba896f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'transforms',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('transforms', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('transforms')