from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4, UUID

from database.stores.errors import DatabaseError, InvalidId, NotFound


class MemoryStore:
    def __init__(self):
        self._items = dict()

    async def create(self, entity):
        entity.id = uuid4()
        entity.created_at = datetime.now(timezone.utc)
        entity.updated_at = datetime.now(timezone.utc)

        self._items[str(entity.id)] = entity

        try:
            return deepcopy(self._items[str(entity.id)])
        except Exception as error:
            raise DatabaseError(error)

    async def update(self, entity):
        if not entity.id:
            raise InvalidId(None)

        entity_id = str(entity.id)

        if not isinstance(entity.id, UUID):
            raise InvalidId(entity.id)

        entity = self._items[entity_id]

        if not entity:
            return NotFound()

        entity.updated_at = datetime.now()
        self._items[entity_id] = entity

        return entity

    async def find_by_id(self, item_id):
        if not isinstance(item_id, UUID):
            raise InvalidId(item_id)

        try:
            return self._items[str(item_id)]
        except KeyError:
            raise NotFound()
        except Exception as error:
            raise DatabaseError(error)

    async def find_list(self, callback=None):
        data = list(self._items.values());

        if not callback:
            return data

        result = filter(callback, data)

        return list(result)
