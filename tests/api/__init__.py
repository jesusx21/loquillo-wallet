import asyncio

from assertpy import assert_that
from falcon.testing import TestCase as FalconTestCase
from tests.config import TestConfig

from app import create_app
from database import get_database


class TestCase(FalconTestCase):
    def setUp(self):
        super().setUp()

        self._config = self._get_config()

        self._start_event_loop()
        self._config.use_in_memory_database()

        self.app = self._create_app()

    def tearDown(self):
        self._stop_event_loop()

    def assert_that(self, value):
        return assert_that(value)

    def get_database(self):
        return get_database(self._config)

    def wait_for(self, task):
        if not self._is_loop_running():
            self._start_event_loop()

        return self.loop.run_until_complete(task)

    def _create_app(self):
        return create_app(self._config)

    def _start_event_loop(self):
        if self._is_loop_running():
            return self.loop

        self.loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self.loop)

    def _stop_event_loop(self):
        if self._is_loop_running():
            self.loop.close()

    def _is_loop_running(self):
        try:
            return self.loop.is_running()
        except AttributeError:
            return False

    def _get_config(self):
        config = TestConfig('../../config.ini')

        config.use_in_memory_database()

        return config
