"""empty message

Revision ID: 205176618653
Revises: 595de8e5dbb7
Create Date: 2019-04-20 15:04:08.427941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '205176618653'
down_revision = '595de8e5dbb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('charge', sa.Column('to_print', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('charge', 'to_print')
    # ### end Alembic commands ###