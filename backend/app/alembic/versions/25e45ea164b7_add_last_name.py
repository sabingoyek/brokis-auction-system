"""Add last name

Revision ID: 25e45ea164b7
Revises: e3d58eefc9b9
Create Date: 2022-04-06 22:22:53.694094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25e45ea164b7'
down_revision = 'e3d58eefc9b9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('last_name', sa.String(), nullable=True))
    op.create_index(op.f('ix_user_last_name'), 'user', ['last_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_last_name'), table_name='user')
    op.drop_column('user', 'last_name')
    # ### end Alembic commands ###