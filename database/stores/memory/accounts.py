from database.stores.errors import InvalidId, NotFound, AccountNotFound
from database.stores.memory.store import MemoryStore


class AccountsStore:
    def __init__(self):
        self._store = MemoryStore()

    def create(self, account):
        return self._store.create(account)

    async def update(self, account):
        try:
            return await self._store.update(account)
        except NotFound:
            raise AccountNotFound(account.id)

    async def find_by_id(self, id):
        try:
            return await self._store.find_by_id(id)
        except NotFound:
            raise AccountNotFound(id)
