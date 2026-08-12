from sqlalchemy.schema import Column, Table
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.expression import text
from sqlalchemy.types import DateTime, String, Integer

from database.metadata import metadata
from database.types import GUID


Entries = Table(
    'entries',
    metadata,
    Column('id', GUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('transaction_id', GUID, nullable=False),
    Column('account_id', GUID, nullable=False),
    Column('concept', String(256), nullable=False),
    Column('amount', Integer, nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False)
)
