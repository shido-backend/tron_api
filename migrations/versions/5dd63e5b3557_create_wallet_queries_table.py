"""Create wallet_queries table

Revision ID: 5dd63e5b3557
Revises: 
Create Date: 2025-03-26 14:00:31.523239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5dd63e5b3557'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wallet_queries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('bandwidth', sa.Integer(), nullable=True),
    sa.Column('energy', sa.Integer(), nullable=True),
    sa.Column('trx_balance', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wallet_queries_address'), 'wallet_queries', ['address'], unique=False)
    op.create_index(op.f('ix_wallet_queries_id'), 'wallet_queries', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wallet_queries_id'), table_name='wallet_queries')
    op.drop_index(op.f('ix_wallet_queries_address'), table_name='wallet_queries')
    op.drop_table('wallet_queries')
    # ### end Alembic commands ###
