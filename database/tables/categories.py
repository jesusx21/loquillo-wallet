from sqlalchemy import Column, ForeignKey, Table, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime, String

from .metadata import metadata

Categories = Table(
    'categories',
    metadata,
    Column('id', UUID, server_default=text('gen_random_uuid()'), primary_key=True),
    Column('name', String(256), nullable=False),
    Column('type', String(15), nullable=False),
    Column('account_id', UUID, ForeignKey('accounts.id'), nullable=False),
    Column('user_id', UUID, ForeignKey('users.id'), nullable=False),
    Column('parent_category_id', UUID, ForeignKey('categories.id'), nullable=True),
    Column('created_at', DateTime, server_default=now(), nullable=False),
    Column('updated_at', DateTime, server_default=now(), onupdate=now(), nullable=False),
)
