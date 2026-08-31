from sqlalchemy import Column, Table, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String

from .metadata import metadata

Transactions = Table(
    'transactions',
    metadata,
    Column('id', UUID, server_default=text('gen_random_uuid()'), primary_key=True),
    Column('description', String(500), nullable=False),
    Column('status', String(15), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False)
)
