from .accounts import MemoryAccountsStore
from .entries import MemoryEntriesStore
from .transactions import MemoryTransactionsStore
from .wallets import MemoryWalletsStore


class InMemoryDatabase:
    def __init__(self):
        self.accounts = MemoryAccountsStore()
        self.entries = MemoryEntriesStore()
        self.transactions = MemoryTransactionsStore(self)
        self.wallets = MemoryWalletsStore()
