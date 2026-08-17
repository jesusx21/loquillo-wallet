from sqlalchemy import Column, Table, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String

from .metadata import metadata

Users = Table(
    'users',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('names', String(256), nullable=False),
    Column('last_names', String(256), nullable=False),
    Column('email', String(255), nullable=False, unique=True),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
