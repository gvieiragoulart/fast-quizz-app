"""merge heads

Revision ID: c4a6af98bf1d
Revises: 8730ca2c13c6, a1c3f9d82e47
Create Date: 2026-03-17 22:20:33.020709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4a6af98bf1d'
down_revision: Union[str, None] = ('8730ca2c13c6', 'a1c3f9d82e47')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
