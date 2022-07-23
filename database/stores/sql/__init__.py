from database.stores.sql.wallets import WalletsStore


class SQLDatabase:
    def __init__(self, engine):
        self._engine = engine

        self.wallets = WalletsStore(engine)


__all__ = [
    'WalletsStore'
]
