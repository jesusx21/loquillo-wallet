from sqlalchemy.ext.asyncio import create_async_engine

from tests import TestCase as BaseTestCase

from database.metadata import metadata
from database import get_database


class TestCase(BaseTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self._config.use_sql_database()
        self.engine = self._create_engine()

        async with self.engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    async def asyncTearDown(self):
        await super().asyncTearDown()

        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)

    async def execute(self, statement):
        async with self.engine.begin() as conn:
            return await conn.execute(statement)

    def _create_engine(self):
        return create_async_engine(self._config.get_sql_database_connection_url())
