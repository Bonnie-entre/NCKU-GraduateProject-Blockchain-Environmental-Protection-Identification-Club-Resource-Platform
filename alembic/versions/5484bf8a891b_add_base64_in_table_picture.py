"""add base64 in table Picture

Revision ID: 5484bf8a891b
Revises: 13c8f392a5f3
Create Date: 2023-05-08 18:28:14.378306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5484bf8a891b'
down_revision = '13c8f392a5f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pictures', sa.Column('base64', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pictures', 'base64')
    # ### end Alembic commands ###