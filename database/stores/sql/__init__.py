from database.stores.sql.accounts import AccountsStore
from database.stores.sql.categories import CategoriesStore
from database.stores.sql.wallets import WalletsStore


class SQLDatabase:
    def __init__(self, engine):
        self._engine = engine

        self.accounts = AccountsStore(self, engine)
        self.categories = CategoriesStore(engine)
        self.wallets = WalletsStore(self, engine)


__all__ = [
    'AccountsStore',
    'Categories',
    'WalletsStore'
]
