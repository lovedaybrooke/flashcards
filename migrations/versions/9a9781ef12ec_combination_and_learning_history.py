"""combination and learning history

Revision ID: 9a9781ef12ec
Revises: 428dca497a23
Create Date: 2021-09-04 18:18:02.682658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a9781ef12ec'
down_revision = '428dca497a23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('learning_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('combination_id', sa.Integer(), nullable=True),
    sa.Column('learner_id', sa.Integer(), nullable=True),
    sa.Column('direction', sa.Text(), nullable=True),
    sa.Column('last_correct_date', sa.Date(), nullable=True),
    sa.Column('ease', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['combination_id'], ['combination.id'], ),
    sa.ForeignKeyConstraint(['learner_id'], ['learner.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('learning_history')
    # ### end Alembic commands ###
