"""empty message

Revision ID: 99a51bb81b9f
Revises: None
Create Date: 2019-10-01 20:29:44.985715

"""

# revision identifiers, used by Alembic.
revision = '99a51bb81b9f'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
    sa.Column('name', sa.String(length=1000), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('img', sa.String(length=1000), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=1000), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('tags',
    sa.Column('activity_name', sa.String(length=1000), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_name'], ['activity.name'], ),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('activity_name', 'location_id')
    )
    op.create_table('token',
    sa.Column('token', sa.String(length=1000), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['email'], ['user.email'], ),
    sa.ForeignKeyConstraint(['name'], ['user.name'], ),
    sa.PrimaryKeyConstraint('token')
    )
    op.create_table('trip',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity_name', sa.String(length=1000), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['activity_name'], ['activity.name'], ),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_interests',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('activity_name', sa.String(length=1000), nullable=False),
    sa.ForeignKeyConstraint(['activity_name'], ['activity.name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'activity_name')
    )
    op.create_table('user_locations',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'location_id')
    )
    op.create_table('weather',
    sa.Column('location', sa.Integer(), nullable=False),
    sa.Column('recorded_timestamp', sa.DateTime(), nullable=False),
    sa.Column('weather_timestamp', sa.DateTime(), nullable=False),
    sa.Column('apparent_temperature', sa.Float(), nullable=True),
    sa.Column('cloud_cover', sa.String(length=1000), nullable=True),
    sa.Column('dew_point', sa.Float(), nullable=True),
    sa.Column('humidity', sa.Float(), nullable=True),
    sa.Column('icon', sa.String(length=1000), nullable=True),
    sa.Column('ozone', sa.Float(), nullable=True),
    sa.Column('precip_accumulation', sa.Float(), nullable=True),
    sa.Column('precip_intensity', sa.Float(), nullable=True),
    sa.Column('precip_probability', sa.Float(), nullable=True),
    sa.Column('precip_type', sa.Float(), nullable=True),
    sa.Column('pressure', sa.Float(), nullable=True),
    sa.Column('summary', sa.String(length=1000), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('uvIndex', sa.Float(), nullable=True),
    sa.Column('visibility', sa.Float(), nullable=True),
    sa.Column('windBearing', sa.Float(), nullable=True),
    sa.Column('windGust', sa.Float(), nullable=True),
    sa.Column('windSpeed', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['location'], ['location.id'], ),
    sa.PrimaryKeyConstraint('location', 'recorded_timestamp', 'weather_timestamp')
    )
    op.create_table('trips',
    sa.Column('trip_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('trip_id', 'user_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trips')
    op.drop_table('weather')
    op.drop_table('user_locations')
    op.drop_table('user_interests')
    op.drop_table('trip')
    op.drop_table('token')
    op.drop_table('tags')
    op.drop_table('user')
    op.drop_table('location')
    op.drop_table('activity')
    ### end Alembic commands ###
