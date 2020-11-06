"""empty message

Revision ID: 697e69edbe82
Revises: 3b9aaeb6a516
Create Date: 2020-11-04 17:23:52.681288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '697e69edbe82'
down_revision = '3b9aaeb6a516'
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