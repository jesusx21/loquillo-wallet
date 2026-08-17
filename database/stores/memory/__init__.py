from contextlib import asynccontextmanager

from .accounts import MemoryAccountsStore
from .entries import MemoryEntriesStore
from .transactions import MemoryTransactionsStore
from .users import MemoryUsersStore
from .wallets import MemoryWalletsStore


class InMemoryDatabase:
    def __init__(self):
        self.accounts = MemoryAccountsStore()
        self.entries = MemoryEntriesStore()
        self.transactions = MemoryTransactionsStore(self)
        self.users = MemoryUsersStore()
        self.wallets = MemoryWalletsStore()

    @asynccontextmanager
    async def transacting(self):
        yield self

    async def commit(self): pass

    async def rollback(self, error):
        raise error

    async def execute(self, statement): pass
