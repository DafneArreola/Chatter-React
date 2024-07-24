"""empty message

Revision ID: d68e7b84e571
Revises: 9b8bc92f89e3
Create Date: 2024-07-24 03:59:00.937505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd68e7b84e571'
down_revision = '9b8bc92f89e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('season_number', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('episode_number', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('media_type', sa.String(length=50), nullable=True))

    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.add_column(sa.Column('season_number', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('episode_number', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('media_type', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.drop_column('media_type')
        batch_op.drop_column('episode_number')
        batch_op.drop_column('season_number')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_column('media_type')
        batch_op.drop_column('episode_number')
        batch_op.drop_column('season_number')

    # ### end Alembic commands ###
