from uuid import UUID

from database.stores.errors import EntryNotFound, NotFound
from database.stores.memory.store import MemoryStore
from domain.entities import Entry


class MemoryEntriesStore(MemoryStore[Entry]):
    async def update(self, entry: Entry):
        try:
            return await super().update(entry)
        except NotFound as error:
            raise EntryNotFound(entry.id) from error

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise EntryNotFound(id) from error
