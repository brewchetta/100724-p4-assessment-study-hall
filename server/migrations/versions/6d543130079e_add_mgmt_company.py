"""add mgmt company

Revision ID: 6d543130079e
Revises: 846851e1d86d
Create Date: 2024-12-12 10:59:51.339054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d543130079e'
down_revision = '846851e1d86d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('landlords_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mgmt_company', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('landlords_table', schema=None) as batch_op:
        batch_op.drop_column('mgmt_company')

    # ### end Alembic commands ###
