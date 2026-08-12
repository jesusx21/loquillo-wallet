from .accounts import AccountsStore
from .categories import CategoriesStore
from .entries import EntriesStore
from .transactions import TransactionsStore
from .wallets import WalletsStore


class InMemoryDatabase:
    def __init__(self):
        self.accounts = AccountsStore()
        self.categories = CategoriesStore()
        self.entries = EntriesStore()
        self.transactions = TransactionsStore()
        self.wallets = WalletsStore()
