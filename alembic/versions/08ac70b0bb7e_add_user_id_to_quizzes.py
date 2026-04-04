"""add_user_id_to_quizzes

Revision ID: 08ac70b0bb7e
Revises: c4a6af98bf1d
Create Date: 2026-03-30 00:43:02.124727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08ac70b0bb7e'
down_revision: Union[str, None] = 'c4a6af98bf1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('quizzes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.UUID(), nullable=True))
        batch_op.create_foreign_key('fk_quizzes_user_id', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    with op.batch_alter_table('quizzes', schema=None) as batch_op:
        batch_op.drop_constraint('fk_quizzes_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')
