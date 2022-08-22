from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from database.stores.errors import DatabaseError, InvalidId, NotFound


class SQLStore:
    def __init__(self, engine, table):
        self._engine = engine
        self._table = table

    async def create(self, **kwargs):
        statement = self._table \
            .insert() \
            .values(**kwargs) \
            .returning('*')

        try:
            cursor = await self.execute(statement)
        except Exception as error:
            raise DatabaseError(error)

        return dict(cursor.one())

    async def update(self, **kwargs):
        if 'id' not in kwargs:
            raise InvalidId(None)

        id = kwargs['id']

        if not isinstance(id, UUID):
            raise InvalidId(id)

        statement = self._table \
            .update() \
            .returning('*') \
            .where(self._table.c.id == id) \
            .values(
                updated_at=datetime.now(),
                **kwargs
            )

        try:
            cursor = await self.execute(statement)

            return dict(cursor.one())
        except NoResultFound as error:
            raise NotFound(id) from error
        except Exception as error:
            raise DatabaseError(error)

    def find_by_id(self, id):
        if not isinstance(id, UUID):
            raise InvalidId(id)

        return self.find_one(self._table.c.id == id)

    async def find_list(self, *args, **kwargs):
        if 'statement' in kwargs:
            statement = kwargs['statement']
        else:
            statement = self._table \
                .select() \
                .where(*args)

        try:
            cursor = await self.execute(statement)
            result = map(dict, cursor.all())
        except Exception as error:
            raise DatabaseError(error)

        return list(result)

    async def find_one(self, *query):
        statement = self._table \
            .select() \
            .where(*query)

        try:
            cursor = await self.execute(statement)

            return dict(cursor.one())
        except NoResultFound as error:
            raise NotFound() from error
        except Exception as error:
            raise DatabaseError(error)

    async def execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)
