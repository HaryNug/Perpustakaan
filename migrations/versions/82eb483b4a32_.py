"""empty message

Revision ID: 82eb483b4a32
Revises: 9250ca4c2f10
Create Date: 2023-06-14 13:48:11.316959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82eb483b4a32'
down_revision = '9250ca4c2f10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genre_id', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('author_id', sa.String(), nullable=False))
        batch_op.create_foreign_key(None, 'author', ['author_id'], ['id'])
        batch_op.create_foreign_key(None, 'genre', ['genre_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('author_id')
        batch_op.drop_column('genre_id')

    # ### end Alembic commands ###
