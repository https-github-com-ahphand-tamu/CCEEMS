"""Update Requests table with outreach date field 2

Revision ID: 04fd691b3547
Revises: 180a07954c83
Create Date: 2023-09-26 23:11:10.948254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04fd691b3547'
down_revision = '180a07954c83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('new_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.String(length=80), nullable=False),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('num_of_children', sa.Integer(), nullable=False),
    sa.Column('outreach_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('new-requests')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('new-requests',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"new-requests_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('num_of_children', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('outreach_date', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='new-requests_pkey')
    )
    op.drop_table('new_requests')
    # ### end Alembic commands ###