from database.stores.errors import InvalidId, NotFound, CategoryNotFound
from database.stores.memory.store import MemoryStore


class CategoriesStore:
    def __init__(self):
        self._store = MemoryStore()

    def create(self, name):
        return self._store.create(name=name)

    async def find_by_id(self, id):
        try:
            return await self._store.find_by_id(id)
        except NotFound:
            raise CategoryNotFound(id)

    def find_all(self):
        return self._store.find_list()
