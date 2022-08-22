from sqlalchemy.schema import Column, Table, ForeignKey, PrimaryKeyConstraint, UniqueConstraint

from database.metadata import metadata
from database.types import GUID


WalletsCategories = Table(
    'wallets_categories',
    metadata,
    Column('wallet_id', GUID, ForeignKey('wallets.id'), nullable=False),
    Column('category_id', GUID, ForeignKey('categories.id'), nullable=False),
    PrimaryKeyConstraint('wallet_id', 'category_id')
)
