"""add estimated_time and feedback_mode to quizzes

Revision ID: a1c3f9d82e47
Revises: bf3b4863e394
Create Date: 2026-03-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1c3f9d82e47'
down_revision: Union[str, None] = 'bf3b4863e394'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('quizzes', sa.Column('estimated_time', sa.SmallInteger(), nullable=True))
    op.add_column('quizzes', sa.Column('feedback_mode', sa.String(20), nullable=False, server_default='final'))


def downgrade() -> None:
    op.drop_column('quizzes', 'feedback_mode')
    op.drop_column('quizzes', 'estimated_time')
