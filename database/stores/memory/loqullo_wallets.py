from uuid import UUID

from database.stores.errors import DatabaseError
from database.stores.memory.store import MemoryStore
from domain.entities import LoquilloWallet


class MemoryLoquilloWalletsStore(MemoryStore[LoquilloWallet]):
    async def find_by_user_id(self, user_id: UUID):
        try:
            return await super()._find_one(user_id=user_id)
        except Exception as error:
            raise DatabaseError(user_id) from error
