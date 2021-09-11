"""add last_asked_date

Revision ID: ba6cafc7ac7f
Revises: 9a9781ef12ec
Create Date: 2021-09-11 21:00:19.818328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba6cafc7ac7f'
down_revision = '9a9781ef12ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('learning_history', sa.Column('last_asked_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('learning_history', 'last_asked_date')
    # ### end Alembic commands ###