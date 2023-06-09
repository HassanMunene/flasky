"""I have created another field in the User model that will confirm user account

Revision ID: 43a0495ec5f8
Revises: 66586a711b6a
Create Date: 2023-05-20 12:56:18.546468

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43a0495ec5f8'
down_revision = '66586a711b6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('confirmed')

    # ### end Alembic commands ###
