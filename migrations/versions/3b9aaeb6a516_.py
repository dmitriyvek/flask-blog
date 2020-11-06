"""empty message

Revision ID: 3b9aaeb6a516
Revises: 7c09ba24e899
Create Date: 2020-11-04 17:22:21.453838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b9aaeb6a516'
down_revision = '7c09ba24e899'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_author_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_author_id_fkey', 'posts', 'users', ['author_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
