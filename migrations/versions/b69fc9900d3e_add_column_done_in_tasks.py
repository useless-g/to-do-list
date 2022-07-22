"""add column done in tasks

Revision ID: b69fc9900d3e
Revises: 5820f8ff13ca
Create Date: 2022-07-15 20:21:15.728411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b69fc9900d3e'
down_revision = '5820f8ff13ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('done', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'done')
    # ### end Alembic commands ###
