import os


from assertpy import assert_that
from unittest import IsolatedAsyncioTestCase
from tests.config import TestConfig

from database import get_database


class TestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._config = self._get_config()
        self._config.use_in_memory_database()

    def get_database(self):
        return get_database(self._config)

    def assert_that(self, value):
        return assert_that(value)

    def _get_config(self):
        return TestConfig(self._get_config_path())

    def _get_config_path(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.normpath(os.path.join(dir_path, '..', 'config.ini'))
