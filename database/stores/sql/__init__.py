from .accounts import AccountsStore
from .categories import CategoriesStore
from .entries import EntriesStore
from .transactions import TransactionsStore
from .wallets import WalletsStore


class SQLDatabase:
    def __init__(self, engine):
        self._engine = engine

        self.accounts = AccountsStore(self, engine)
        self.categories = CategoriesStore(self, engine)
        self.entries = EntriesStore(self, engine)
        self.transactions = TransactionsStore(self, engine)
        self.wallets = WalletsStore(self, engine)
