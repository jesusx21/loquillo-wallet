from database.stores.sql.accounts import AccountsStore
from database.stores.sql.wallets import WalletsStore


class SQLDatabase:
    def __init__(self, engine):
        self._engine = engine

        self.accounts = AccountsStore(engine)
        self.wallets = WalletsStore(engine)


__all__ = [
    'AccountsStore',
    'WalletsStore'
]
