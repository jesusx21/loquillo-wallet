from uuid import UUID

from database.stores.errors import EventNotFound, NotFound
from database.stores.memory.store import MemoryStore
from domain.core import Event


class MemoryEventsStore(MemoryStore[Event]):
    async def update(self, event: Event):
        try:
            return await super().update(event)
        except NotFound as error:
            raise EventNotFound(event.id) from error

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise EventNotFound(id) from error
