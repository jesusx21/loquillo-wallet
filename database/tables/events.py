from sqlalchemy import Column, Table, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String, Text

from .metadata import metadata

Events = Table(
    'events',
    metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('type', String(50), nullable=False),
    Column('date', DateTime, server_default=now(), nullable=False),
    Column('metadata', Text(), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False)
)
