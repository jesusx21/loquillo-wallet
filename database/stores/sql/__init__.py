from contextlib import asynccontextmanager

from sqlalchemy import Executable as Statement
from database.stores.sql.events import SQLEventsStore
from sqlalchemy.ext.asyncio import AsyncEngine

from database.stores.sql.categories import SQLCategoriesStore

from .accounts import SQLAccountsStore
from .entries import SQLEntriesStore
from .errors import TransactionNotOpened
from .transactions import SQLTransactionsStore
from .users import SQLUsersStore
from .wallets import SQLWalletsStore


class SQLDatabase:
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

        self.__initialize_stores()

    async def execute(self, statement: Statement):
        async with self._engine.begin() as connection:
            cursor = await connection.execute(statement)

            return cursor.mappings()

    def is_transacting(self):
        return False

    def __initialize_stores(self):
        self.accounts = SQLAccountsStore(self)
        self.categories = SQLCategoriesStore(self)
        self.entries = SQLEntriesStore(self)
        self.events = SQLEventsStore(self)
        self.transactions = SQLTransactionsStore(self)
        self.users = SQLUsersStore(self)
        self.wallets = SQLWalletsStore(self)

    @asynccontextmanager
    async def transacting(self):
        database = SQLTransactionDatabase(self._engine)

        async with database.transacting():
            yield database


class SQLTransactionDatabase(SQLDatabase):
    async def execute(self, statement):
        if not self._has_open_connection():
            raise TransactionNotOpened()

        cursor = await self._connection.execute(statement)

        return cursor.mappings()

    @asynccontextmanager
    async def transacting(self):
        async with self._engine.connect() as connection:
            self._connection = connection

            async with connection.begin() as transaction:
                self._transaction = transaction

                yield self

    def is_transacting(self):
        return hasattr(self, '_transaction') and self._transaction is not None

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
