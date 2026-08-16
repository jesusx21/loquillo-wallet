from sqlalchemy import BigInteger, Column, Table, text
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String, UUID

from .metadata import metadata

Entries = Table(
    'entries',
    metadata,
    Column('id', UUID, server_default=text('gen_random_uuid()'), primary_key=True),
    Column('account_id', UUID, nullable=False),
    Column('transaction_id', UUID, nullable=True),
    Column('concept', String(255), nullable=False),
    Column('amount', BigInteger, nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
