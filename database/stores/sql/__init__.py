from contextlib import asynccontextmanager

from sqlalchemy import Executable as Statement
from sqlalchemy.ext.asyncio import AsyncEngine

from .errors import TransactionNotOpened
from database.stores.sql.accounts import SQLAccountsStore
from database.stores.sql.entries import SQLEntriesStore
from database.stores.sql.transactions import SQLTransactionsStore
from database.stores.sql.wallets import SQLWalletsStore


class SQLDatabase:
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

        self.__initialize_stores()

    async def execute(self, statement: Statement):
        async with self._engine.begin() as connection:
            cursor = await connection.execute(statement)

            return cursor.mappings()

    def __initialize_stores(self):
        self.accounts = SQLAccountsStore(self)
        self.entries = SQLEntriesStore(self)
        self.transactions = SQLTransactionsStore(self)
        self.wallets = SQLWalletsStore(self)


class SQLTransactionDatabase(SQLDatabase):
    @asynccontextmanager
    async def transacting(self):
        async with self._engine.connect() as connection:
            self._connection = await connection.execution_options(isolation_level='REPEATABLE READ')

            async with self._connection.begin() as transaction:
                self._transaction = transaction

                try:
                    yield self

                    await self.commit()
                except Exception as error:
                    await self.rollback(error)

    async def execute(self, statement):
        if not self._has_open_connection():
            raise TransactionNotOpened()

        cursor = await self._connection.execute(statement)

        return cursor.mappings()

    async def commit(self):
        if not self._has_open_connection():
            raise TransactionNotOpened()

        await self._transaction.commit()

    async def rollback(self, error):
        if not self._has_open_connection():
            raise TransactionNotOpened()

        await self._transaction.rollback()

        raise error

    def _has_open_connection(self):
        return hasattr(self, '_connection')
