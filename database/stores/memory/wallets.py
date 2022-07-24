from database.stores.errors import NotFound, WalletNotFound
from database.stores.memory.store import MemoryStore


class WalletsStore:
    def __init__(self):
        self._store = MemoryStore()

    async def create(self, name):
        return await self._store.create({'name': name})

    async def find_by_id(self, id):
        try:
            return await self._store.find_by_id(id)
        except NotFound:
            raise WalletNotFound(id)
