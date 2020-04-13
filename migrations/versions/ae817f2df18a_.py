"""empty message

Revision ID: ae817f2df18a
Revises: 60ff3f7a5098
Create Date: 2019-11-24 11:20:08.552763

"""

# revision identifiers, used by Alembic.
revision = "ae817f2df18a"
down_revision = "60ff3f7a5098"

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("has_toured", sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "has_toured")
    ### end Alembic commands ###
