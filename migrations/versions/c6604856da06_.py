"""empty message

Revision ID: c6604856da06
Revises: 47cd5fe99d32
Create Date: 2020-04-18 16:49:39.265650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6604856da06'
down_revision = '47cd5fe99d32'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('most_recent_invite', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'most_recent_invite')
    ### end Alembic commands ###
