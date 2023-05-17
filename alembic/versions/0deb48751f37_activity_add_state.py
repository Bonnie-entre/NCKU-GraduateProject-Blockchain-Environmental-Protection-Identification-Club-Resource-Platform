"""activity add state

Revision ID: 0deb48751f37
Revises: 4ece259f936e
Create Date: 2023-05-17 21:47:20.519506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0deb48751f37'
down_revision = '4ece259f936e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('state', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activities', 'state')
    # ### end Alembic commands ###