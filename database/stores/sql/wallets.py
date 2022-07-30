from uuid import UUID

from sqlalchemy.exc import NoResultFound

from database.tables import Wallets
from database.stores.errors import DatabaseError, InvalidId, WalletNotFound


class WalletsStore:
    def __init__(self, engine):
        self._engine = engine

    async def create(self, name):
        statement = Wallets \
            .insert() \
            .values(name=name)

        try:
            cursor = await self._execute(statement)
        except Exception as error:
            raise DatabaseError(error)

        return await self.find_by_id(cursor.inserted_primary_key[0])

    async def find_by_id(self, id):
        if not isinstance(id, UUID):
            raise InvalidId(id)

        statement = Wallets \
            .select() \
            .where(Wallets.c.id == id)

        try:
            cursor = await self._execute(statement)

            return dict(cursor.one())
        except NoResultFound as error:
            raise WalletNotFound(id) from error
        except Exception as error:
            raise DatabaseError(error)

    async def find_all(self):
        statement = Wallets \
            .select()

        try:
            cursor = await self._execute(statement)
            result = map(dict, cursor.all())
        except Exception as error:
            raise DatabaseError(error)

        return list(result)

    async def _execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)
