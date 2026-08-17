from uuid import UUID

from database.stores.errors import NotFound, UserNotFound
from database.stores.memory.store import MemoryStore
from domain.entities import User


class MemoryUsersStore(MemoryStore[User]):
    async def update(self, user: User):
        try:
            return await super().update(user)
        except NotFound as error:
            raise UserNotFound(user.id) from error

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise UserNotFound(id) from error
