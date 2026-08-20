from copy import deepcopy
from datetime import datetime, timezone
from typing import Generic, TypeVar
from uuid import UUID, uuid4

from database.stores.errors import InvalidId, NotFound

Entity = TypeVar('Entity')


class MemoryStore(Generic[Entity]):
    def __init__(self):
        self.__items: dict[str, Entity] = {}

    async def create(self, entity: Entity) -> Entity:
        if not entity.id:
            entity.id = uuid4()
        entity.created_at = datetime.now(timezone.utc)
        entity.updated_at = datetime.now(timezone.utc)

        self.__items[str(entity.id)] = deepcopy(entity)

        return self.__items[str(entity.id)]

    async def find_by_id(self, item_id: UUID) -> Entity:
        if not isinstance(item_id, UUID):
            raise InvalidId(item_id)

        try:
            return deepcopy(self.__items[str(item_id)])
        except KeyError as error:
            raise NotFound() from error

    async def update(self, entity: Entity) -> Entity:
        if not entity.id:
            raise InvalidId(None)

        if not isinstance(entity.id, UUID):
            raise InvalidId(entity.id)

        entity_id = str(entity.id)

        if entity_id not in self.__items:
            raise NotFound()

        entity_to_update = deepcopy(self.__items[entity_id])
        entity_to_update.updated_at = datetime.now(timezone.utc)
        self.__items[entity_id] = deepcopy(entity_to_update)

        return entity_to_update

    async def _find_one(self, **kwargs) -> Entity:
        entities = await self._find(**kwargs)

        if not entities:
            raise NotFound()

        return entities[0]

    async def _find(self, **kwargs) -> list[Entity]:
        result = filter(
            lambda entity: all(
                getattr(entity, key) in value
                if isinstance(value, list)
                else getattr(entity, key) == value
                for key, value in kwargs.items()
            ),
            self.__get_entities()
        )

        return list(result)

    def __get_entities(self):
        entities = self.__items.values()
        entities = list(entities)

        return deepcopy(entities)
