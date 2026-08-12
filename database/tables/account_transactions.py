from sqlalchemy.schema import Column, Table
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.expression import text
from sqlalchemy.types import DateTime, String

from database.metadata import metadata
from database.types import GUID


AccountTransactions = Table(
    'account_transactions',
    metadata,
    Column('id', GUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('description', String(256), nullable=False),
    Column('created_at', DateTime, server_default=now(), nullable=False)
)
