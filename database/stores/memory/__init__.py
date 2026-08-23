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

        self._is_transacting = False

    def is_transacting(self):
        return self._is_transacting

    @asynccontextmanager
    async def transacting(self):
        self._is_transacting = True
        try:
            yield self
        finally:
            self._is_transacting = False

    async def commit(self): pass

    async def rollback(self, error):
        raise error

    async def execute(self, statement): pass
