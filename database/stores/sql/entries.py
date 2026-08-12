from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from database.tables import Entries
from database.stores.errors import DatabaseError
from mister_krabz.entities import Entry


class EntriesStore:
    def __init__(self, db, engine):
        self._db = db
        self._engine = engine

    async def create(self, entry):
        statement = Entries \
            .insert() \
            .values(
                concept=entry.concept,
                amount=entry.amount,
                transaction_id=entry.transaction_id,
                account_id=entry.account_id
            ) \
            .returning('*')

        try:
            cursor = await self._execute(statement)

            return self._build_entry(cursor.one())
        except Exception as error:
            raise DatabaseError(error)

    def _build_entry(self, result):
        data = dict(result)

        entry = Entry(**data)

        return entry

    async def _execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)

