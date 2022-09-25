from sqlalchemy.schema import Column, Table, ForeignKey
from sqlalchemy.sql.expression import text

from database.metadata import metadata
from database.types import GUID


WalletsCategories = Table(
    'wallets_categories',
    metadata,
    Column('id', GUID, server_default=text('gen_random_uuid()'), primary_key=True),
    Column('account_id', GUID, ForeignKey('accounts.id'), nullable=False),
    Column('category_id', GUID, ForeignKey('categories.id'), nullable=False),
    Column('wallet_id', GUID, ForeignKey('wallets.id'), nullable=False)
)
