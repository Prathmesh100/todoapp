"""create phonenumber for phonenumber

Revision ID: 654c5ff331db
Revises: 
Create Date: 2025-02-27 14:54:20.721757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '654c5ff331db'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(10),nullable=True))


def downgrade() -> None:
    op.drop_column('users','phone_number')
