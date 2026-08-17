from uuid import UUID

from database.stores.errors import NotFound, UserNotFound
from database.stores.sql.store import SQLStore
from database.tables import Users
from domain.entities import User


class SQLUsersStore(SQLStore):
    def __init__(self, database: object):
        super().__init__(database, Users)

    async def create(self, user: User):
        return await self._create(
            names=user.names,
            last_names=user.last_names,
            email=user.email
        )

    async def find_by_id(self, user_id: UUID) -> User:
        try:
            return await self._find_by_id(user_id)
        except NotFound as error:
            raise UserNotFound(user_id) from error

    def _build_entity(self, **kwargs) -> User:
        return User(
            id=kwargs['id'],
            names=kwargs['names'],
            last_names=kwargs['last_names'],
            email=kwargs['email'],
            created_at=kwargs['created_at'],
            updated_at=kwargs['updated_at']
        )
