from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from database.tables import Transactions
from database.stores.errors import DatabaseError
from mister_krabz.entities import Entry


class TransactionsStore:
    def __init__(self, db, engine):
        self._db = db
        self._engine = engine

    async def create(self, transaction):
        statement = Transactions \
            .insert() \
            .values(description=transaction.description) \
            .returning('*')

        try:
            cursor = await self._execute(statement)

            return self._build_transaction(cursor.one())
        except Exception as error:
            raise DatabaseError(error)

    def _build_transaction(self, result):
        data = dict(result)

        transaction = Transaction(**data)

        return transaction

    async def _execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)

