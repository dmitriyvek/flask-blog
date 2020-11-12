"""empty message

Revision ID: 359fc77c4965
Revises: d7ba141e7cc2
Create Date: 2020-11-12 13:00:15.365915

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359fc77c4965'
down_revision = 'd7ba141e7cc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('is_deleted', sa.Boolean(), nullable=True, comment='If the post is marked for deletion then it should not be given to the client'))
    op.add_column('users', sa.Column('is_deleted', sa.Boolean(), nullable=True, comment='If the user is marked for deletion then it should not be valid for authentification'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_deleted')
    op.drop_column('posts', 'is_deleted')
    # ### end Alembic commands ###
