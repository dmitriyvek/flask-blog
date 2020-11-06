"""empty message

Revision ID: 5492370dd984
Revises: 7c7e57230343
Create Date: 2020-11-04 17:10:54.028272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5492370dd984'
down_revision = '7c7e57230343'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###