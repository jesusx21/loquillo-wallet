from uuid import UUID

from database.stores.errors import EntryNotFound, NotFound
from domain.entities import Entry
from .store import MemoryStore


class MemoryEntriesStore(MemoryStore[Entry]):
    async def update(self, entry: Entry):
        try:
            return await super().update(entry)
        except NotFound:
            raise EntryNotFound(entry.id)

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound:
            raise EntryNotFound(id)
