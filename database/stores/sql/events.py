from uuid import UUID
import json

from database.stores.errors import EventNotFound, NotFound
from database.stores.sql.store import SQLStore
from database.tables import Events
from domain.core import Event


class SQLEventsStore(SQLStore):
    def __init__(self, database: object):
        super().__init__(database, Events)

    async def create(self, event: Event):
        metadata_json = json.dumps(
            event.get_metadata()
        )

        return await self._create(
            type=event.type,
            date=event.date,
            metadata=metadata_json,
            created_at=event.created_at,
        )

    async def find_by_id(self, event_id: UUID) -> Event:
        try:
            return await self._find_by_id(event_id)
        except NotFound as error:
            raise EventNotFound(event_id) from error

    def _build_entity(self, **kwargs) -> Event:
        return Event(
            id=kwargs['id'],
            date=kwargs['date'],
            created_at=kwargs['created_at'],
            **json.loads(kwargs['metadata'])
        )
