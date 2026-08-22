from sqlalchemy import Column, ForeignKey, Table, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime

from .metadata import metadata


LoquilloWallets = Table(
    'loquillo_wallets',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('user_id', UUID, ForeignKey('users.id'), nullable=False),
    Column('incomes_account_id', UUID, ForeignKey('accounts.id'), nullable=False),
    Column('expenses_account_id', UUID, ForeignKey('accounts.id'), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False),
)
