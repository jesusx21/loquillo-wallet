from copy import deepcopy
from datetime import datetime, timezone
from typing import TypeVar, Generic
from uuid import uuid4, UUID

from database.stores.errors import DatabaseError, InvalidId, NotFound

Entity = TypeVar('Entity')


class MemoryStore(Generic[Entity]):
    def __init__(self):
        self._items: dict[str, Entity] = dict()

    async def create(self, entity: Entity) -> Entity:
        entity.id = uuid4()
        entity.created_at = datetime.now(timezone.utc)
        entity.updated_at = datetime.now(timezone.utc)

        self._items[str(entity.id)] = deepcopy(entity)

        try:
            return self._items[str(entity.id)]
        except Exception as error:
            raise DatabaseError(error)

    async def update(self, entity: Entity) -> Entity:
        if not entity.id:
            raise InvalidId(None)

        if not isinstance(entity.id, UUID):
            raise InvalidId(entity.id)

        entity_id = str(entity.id)

        entity = deepcopy(self._items[entity_id])

        if not entity:
            raise NotFound()

        entity.updated_at = datetime.now()
        self._items[entity_id] = deepcopy(entity)

        return entity

    async def find_by_id(self, item_id: UUID) -> Entity:
        if not isinstance(item_id, UUID):
            raise InvalidId(item_id)

        try:
            return deepcopy(self._items[str(item_id)])
        except KeyError:
            raise NotFound()
        except Exception as error:
            raise DatabaseError(error)

    async def find_list(self, callback=None) -> list[Entity]:
        data = deepcopy(list(self._items.values()))

        if not callback:
            return data

        result = filter(callback, data)

        return list(result)
