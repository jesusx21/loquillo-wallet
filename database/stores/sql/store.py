from uuid import UUID

from sqlalchemy import Executable as Statement, Table
from sqlalchemy.engine import Row
from sqlalchemy.exc import NoResultFound as DoesNotExist
from sqlalchemy.ext.asyncio import AsyncEngine

from database.stores.errors import DatabaseError, InvalidId, NotFound


type SingleResult = Row


class SQLStore:
    def __init__(self, engine: AsyncEngine, table: Table):
        self.__engine = engine
        self._table = table

    async def _create(self, **data):
        statement = self._table \
            .insert() \
            .values(**data) \
            .returning('*')

        try:
            cursor = await self._execute(statement)

            return self.__format_input(cursor.one())
        except Exception as error:
            raise DatabaseError(cause=error)

    async def _find_by_id(self, entity_id: UUID):
        if not isinstance(entity_id, UUID):
            raise InvalidId(entity_id)

        statement = self._table \
            .select() \
            .where(self._table.c.id == entity_id)

        try:
            cursor = await self._execute(statement)

            return self.__format_input(cursor.one())
        except DoesNotExist as error:
            raise NotFound(entity_id) from error
        except Exception as error:
            raise DatabaseError(cause=error)

    def _build_entity(self, **kwargs):
        raise NotImplementedError('Subclasses must implement this method')

    async def _execute(self, statement: Statement):
        async with self.__engine.begin() as connection:
            cursor = await connection.execute(statement)

            return cursor.mappings()

    def __format_input(self, result: SingleResult):
        data: dict[str, any] = dict(result)

        return self._build_entity(**data)
