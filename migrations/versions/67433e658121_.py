"""empty message

Revision ID: 67433e658121
Revises: 99f67636cbe6
Create Date: 2020-11-04 17:33:00.092912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67433e658121'
down_revision = '99f67636cbe6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
