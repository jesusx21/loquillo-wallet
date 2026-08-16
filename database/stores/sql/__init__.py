from sqlalchemy.ext.asyncio import AsyncEngine

from database.stores.sql.accounts import SQLAccountsStore
from database.stores.sql.entries import SQLEntriesStore
from database.stores.sql.transactions import SQLTransactionsStore


class SQLDatabase:
    def __init__(self, engine: AsyncEngine):
        self.__engine = engine

        self.accounts = SQLAccountsStore(self.__engine)
        self.entries = SQLEntriesStore(self.__engine)
        self.transactions = SQLTransactionsStore(self.__engine)
