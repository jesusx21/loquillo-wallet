from copy import deepcopy
from datetime import datetime, timezone
from uuid import uuid4, UUID

from database.stores.errors import DatabaseError, InvalidId, NotFound


class MemoryStore:
    def __init__(self):
        self._items = dict()

    async def create(self, data):
        data['id'] = uuid4()
        data['created_at'] = datetime.now(timezone.utc)
        data['updated_at'] = datetime.now(timezone.utc)

        self._items[str(data['id'])] = data

        try:
            return deepcopy(self._items[str(data['id'])])
        except Exception as error:
            raise DatabaseError(error)

    async def update(self, record):
        if 'id' not in record:
            raise InvalidId(None)

        record_id = str(record['id'])

        if not isinstance(record['id'], UUID):
            raise InvalidId(record['id'])

        record = self._items[record_id]

        if not record:
            return NotFound()

        record['updated_at'] = datetime.now()
        self._items[record_id] = record

        return record

    async def find_by_id(self, item_id):
        if not isinstance(item_id, UUID):
            raise InvalidId(item_id)

        try:
            return deepcopy(self._items[str(item_id)])
        except KeyError:
            raise NotFound()
        except Exception as error:
            raise DatabaseError(error)

    async def find_all(self):
        return list(self._items.values());
