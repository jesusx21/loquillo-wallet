from sqlalchemy import Column, ForeignKey, Table, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String

from .metadata import metadata


Wallets = Table(
    'wallets',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('name', String(256), nullable=False),
    Column('type', String(25), nullable=False),
    Column('account_id', UUID, ForeignKey('accounts.id'), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
