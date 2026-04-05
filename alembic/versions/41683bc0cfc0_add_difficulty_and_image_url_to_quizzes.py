"""add difficulty and image_url to quizzes

Revision ID: 41683bc0cfc0
Revises: 08ac70b0bb7e
Create Date: 2026-04-05 17:24:55.162693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41683bc0cfc0'
down_revision: Union[str, None] = '08ac70b0bb7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('quizzes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('difficulty', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('image_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('quizzes', schema=None) as batch_op:
        batch_op.drop_column('image_url')
        batch_op.drop_column('difficulty')
