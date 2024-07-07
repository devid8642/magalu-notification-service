"""communication_type field renamed to channel

Revision ID: 3813a7f9964b
Revises: bb4c4063bc91
Create Date: 2024-07-07 14:48:35.961116

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3813a7f9964b'
down_revision: Union[str, None] = 'bb4c4063bc91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


channels_enum = sa.Enum('EMAIL', 'SMS', 'PUSH', 'WHATSAPP', name='channels')


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    channels_enum.create(op.get_bind())
    op.add_column('notifications', sa.Column('channel', channels_enum, nullable=False))
    op.drop_column('notifications', 'communication_type')
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifications', sa.Column('communication_type', postgresql.ENUM('EMAIL', 'SMS', 'PUSH', 'WHATSAPP', name='communicationtype'), autoincrement=False, nullable=False))
    op.drop_column('notifications', 'channel')
    channels_enum.drop(op.get_bind())
    # ### end Alembic commands ###