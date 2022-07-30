from sqlalchemy.schema import Column, Table
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String

from database.metadata import metadata
from database.types import GUID

Wallets = Table(
    'wallets',
    metadata,
    Column('id', GUID, primary_key=True),
    Column('name', String(256), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
