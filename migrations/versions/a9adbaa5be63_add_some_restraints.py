"""add some restraints

Revision ID: a9adbaa5be63
Revises: b69fc9900d3e
Create Date: 2022-07-15 20:33:47.617148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9adbaa5be63'
down_revision = 'b69fc9900d3e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('tasks', 'text',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'text',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('tasks', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
