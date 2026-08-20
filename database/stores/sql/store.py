from uuid import UUID
from enum import Enum

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
        where_clauses = self.__format_where_clause(**filters)

        statement = self.__table \
            .select() \
            .where(*where_clauses)

        try:
            cursor = await self._execute(statement)

            return self.__format_input(cursor.one())
        except DoesNotExist as error:
            raise NotFound(filters) from error
        except Exception as error:
            raise DatabaseError(cause=error)

    async def _find(self, **filters):
        where_clauses = self.__format_where_clause(**filters)

        statement = self.__table \
            .select() \
            .where(*where_clauses)

        try:
            cursor = await self._execute(statement)

            return [self.__format_input(row) for row in cursor.fetchall()]
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

    def __format_where_clause(self, **filters):
        where_clauses = []

        for key, value in filters.items():
            formatted_value = self.__format_where_clause_value(value)
            column = self.__table.c[key]

            if isinstance(value, list):
                where_clauses.append(column.in_(formatted_value))
                continue

            where_clauses.append(column == formatted_value)

        return where_clauses

    def __format_where_clause_value(self, value):
        if isinstance(value, list):
            return [self.__format_where_clause_value(v) for v in value]
        elif isinstance(value, Enum):
            return value.value
        else:
            return value
