from uuid import UUID

from sqlalchemy import Executable as Statement, MappingResult, Table
from sqlalchemy.engine import Row
from sqlalchemy.exc import NoResultFound as DoesNotExist

from database.stores.errors import DatabaseError, InvalidId, NotFound


type SingleResult = Row


class SQLStore:
    def __init__(self, database: object, table: Table):
        self._database = database
        self.__table = table

    async def _create(self, **data):
        statement = self.__table \
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

        statement = self.__table \
            .select() \
            .where(self.__table.c.id == entity_id)

        try:
            cursor = await self._execute(statement)

            return self.__format_input(cursor.one())
        except DoesNotExist as error:
            raise NotFound(entity_id) from error
        except Exception as error:
            raise DatabaseError(cause=error)

    async def _find_one(self, **filters):
        statement = self.__table \
            .select() \
            .where(*[self.__table.c[key] == value for key, value in filters.items()])

        try:
            cursor = await self._execute(statement)

            return self.__format_input(cursor.one())
        except DoesNotExist as error:
            raise NotFound(filters) from error
        except Exception as error:
            raise DatabaseError(cause=error)

    def _build_entity(self, **kwargs):
        raise NotImplementedError('Subclasses must implement this method')

    async def _execute(self, statement: Statement) -> MappingResult:
        return await self._database.execute(statement)

    def __format_input(self, result: SingleResult):
        data: dict[str, any] = dict(result)

        return self._build_entity(**data)
