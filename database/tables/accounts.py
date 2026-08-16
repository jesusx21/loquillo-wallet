from sqlalchemy import Column, Table, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String

from .metadata import metadata

Accounts = Table(
    'accounts',
    metadata,
    Column('id', UUID, server_default=text('gen_random_uuid()'), primary_key=True),
    Column('name', String(256), nullable=False),
    Column('type', String(20), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
