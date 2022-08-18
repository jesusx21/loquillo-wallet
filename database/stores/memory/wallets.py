from database.stores.errors import InvalidId, NotFound, WalletNotFound
from database.stores.memory.store import MemoryStore


class WalletsStore:
    def __init__(self):
        self._store = MemoryStore()

    async def create(self, wallet):
        return await self._store.create(wallet)

    async def update(self, wallet):
        try:
            return await self._store.update(wallet)
        except NotFound:
            raise WalletNotFound(wallet.id)

    async def update(self, wallet):
        try:
            return await self._store.update(wallet)
        except NotFound:
            raise WalletNotFound(wallet['id'])

    async def find_by_id(self, id):
        try:
            return await self._store.find_by_id(id)
        except NotFound:
            raise WalletNotFound(id)

    async def find_all(self):
        return await self._store.find_list()
