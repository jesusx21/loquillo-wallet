import asyncio

from assertpy import assert_that
from unittest import IsolatedAsyncioTestCase

from database.stores import InMemoryDatabase
from tests.config import TestConfig


class TestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        asyncio.get_running_loop().slow_callback_duration = 0.5

        await self.async_set_up()

    async def asyncTearDown(self):
        await self.async_tear_down()
        await super().asyncTearDown()

    async def async_set_up(self):
        self._config = TestConfig()

    async def async_tear_down(self):
        pass

    def setUp(self):
        self.set_up()

    def tearDown(self):
        self.tear_down()

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def get_database(self) -> InMemoryDatabase:
        return InMemoryDatabase()

    def assert_that(self, value):
        return assert_that(value)
