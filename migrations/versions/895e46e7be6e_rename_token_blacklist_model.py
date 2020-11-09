"""rename token blacklist model

Revision ID: 895e46e7be6e
Revises: f4912ffbe3a1
Create Date: 2020-11-07 12:04:06.868128

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '895e46e7be6e'
down_revision = 'f4912ffbe3a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.drop_table('token_blacklist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_blacklist',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('blacklisted_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='token_blacklist_pkey'),
    sa.UniqueConstraint('token', name='token_blacklist_token_key')
    )
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###