import os

from sqlalchemy.ext.asyncio import create_async_engine

from assertpy import assert_that
from unittest import IsolatedAsyncioTestCase
from tests.config import TestConfig

from database.metadata import metadata
from database import get_database


class TestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._config = self._get_config()
        self.engine = self._create_engine()

        async with self.engine.begin() as connection:
            await connection.run_sync(metadata.create_all)

    async def asyncTearDown(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.drop_all)

    async def get_database(self):
        return get_database(self._config)

    async def execute(self, statement):
        async with self.engine.begin() as conn:
            return await conn.execute(statement)

    def assert_that(self, value):
        return assert_that(value)

    def _create_engine(self):
        return create_async_engine(self._config.get_sql_database_connection_url())

    def _get_config(self):
        config = TestConfig(self._get_config_path())

        config.use_sql_database()

        return config

    def _get_config_path(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.normpath(os.path.join(dir_path, '../..', 'config.ini'))
