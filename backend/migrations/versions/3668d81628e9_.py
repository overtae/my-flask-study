"""empty message

Revision ID: 3668d81628e9
Revises: 5c88c3931dad
Create Date: 2022-12-16 23:32:18.505113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3668d81628e9'
down_revision = '5c88c3931dad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_liker',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['Post.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_liker')
    # ### end Alembic commands ###