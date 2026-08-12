from .accounts import MemoryAccountsStore
from .entries import MemoryEntriesStore
from .transactions import MemoryTransactionsStore


class InMemoryDatabase:
    def __init__(self):
        self.accounts = MemoryAccountsStore()
        self.entries = MemoryEntriesStore()
        self.transactions = MemoryTransactionsStore()
