import os

from assertpy import assert_that
from unittest import IsolatedAsyncioTestCase
from mister_krabz.entities.account import Account
from tests.config import TestConfig

from database import get_database
from mister_krabz import Wallets


class TestCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._config = self._get_config()
        self._config.use_in_memory_database()

    def get_database(self):
        return get_database(self._config)

    def assert_that(self, value):
        return assert_that(value)

    def create_account(self, database, name):
        account = Account(name=f'{name} Transactions')

        return database.accounts.create(account)

    def create_wallet(self, database, name):
        wallets = Wallets(database)

        return wallets.create(name=name)

    def _get_config(self):
        return TestConfig(self._get_config_path())

    def _get_config_path(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        return os.path.normpath(os.path.join(dir_path, '..', 'config.ini'))
