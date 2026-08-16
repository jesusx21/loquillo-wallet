from sqlalchemy.ext.asyncio import create_async_engine

from tests import TestCase

from database.stores import SQLDatabase
from database.tables.metadata import metadata


class SQLTestCase(TestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self._config.use_sql_database()
        self.engine = self.__create_engine()

        async with self.engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    async def async_tear_down(self):
        await super().async_tear_down()

        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)

    def get_database(self):
        return SQLDatabase(self.engine)

    def __create_engine(self):
        return create_async_engine(self._config.sql_connection_uri)
