from assertpy import assert_that
from unittest import IsolatedAsyncioTestCase

from database import get_database
from database.stores import InMemoryDatabase


class TestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        await self.async_set_up()

    async def asyncTearDown(self):
        await self.async_tear_down()
        await super().asyncTearDown()

    async def async_set_up(self):
        pass

    async def async_tear_down(self):
        pass

    def get_database(self) -> InMemoryDatabase:
        return get_database()

    def assert_that(self, value):
        return assert_that(value)
