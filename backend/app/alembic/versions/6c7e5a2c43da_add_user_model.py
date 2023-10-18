"""add_user_model

Revision ID: 6c7e5a2c43da
Revises: 
Create Date: 2023-10-18 04:49:04.704333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c7e5a2c43da'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Create the new columns
    op.add_column('user', sa.Column('first_name', sa.String(length=80), nullable=False))
    op.add_column('user', sa.Column('last_name', sa.String(length=80), nullable=False))

def downgrade():
    # Remove the new columns
    op.drop_column('user', 'first_name')
    op.drop_column('user', 'last_name')

