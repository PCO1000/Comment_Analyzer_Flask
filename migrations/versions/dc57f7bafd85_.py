"""empty message

Revision ID: dc57f7bafd85
Revises: 2920577e02cc
Create Date: 2024-02-13 18:17:14.227211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc57f7bafd85'
down_revision = '2920577e02cc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('text', schema=None) as batch_op:
        batch_op.add_column(sa.Column('toxicity_score', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('text', schema=None) as batch_op:
        batch_op.drop_column('toxicity_score')

    # ### end Alembic commands ###
