"""empty message

Revision ID: 9250ca4c2f10
Revises: b5c9f0509282
Create Date: 2023-06-14 13:32:48.837080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9250ca4c2f10'
down_revision = 'b5c9f0509282'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=False))
        batch_op.drop_constraint('book_genre_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('book_author_id_fkey', type_='foreignkey')
        batch_op.drop_column('genre_id')
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('genre_id', sa.VARCHAR(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('book_author_id_fkey', 'author', ['author_id'], ['id'])
        batch_op.create_foreign_key('book_genre_id_fkey', 'genre', ['genre_id'], ['id'])
        batch_op.drop_column('description')

    # ### end Alembic commands ###
