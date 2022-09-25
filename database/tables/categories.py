from sqlalchemy.schema import Column, Table, ForeignKey
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.expression import text
from sqlalchemy.types import DateTime, String

from database.metadata import metadata
from database.types import GUID


Categories = Table(
    'categories',
    metadata,
    Column('id', GUID, server_default=text('gen_random_uuid()'), primary_key=True),
    Column('name', String(256), nullable=False),
    Column('parent_category_id', GUID, ForeignKey('categories.id'), nullable=True),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False)
)
