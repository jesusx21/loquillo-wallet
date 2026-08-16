from sqlalchemy.ext.asyncio import AsyncEngine

from database.stores.sql.accounts import AccountsStore


class SQLDatabase:
    def __init__(self, engine: AsyncEngine):
        self.__engine = engine

        self.accounts = AccountsStore(self.__engine)
