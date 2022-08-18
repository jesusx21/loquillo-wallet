from unittest.mock import patch
from tests import TestCase

from mister_krabz import Wallets
from mister_krabz.errors import CouldntCreateWallet, CouldntGetWallets


class TestWallet(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()
        self.wallets = Wallets(self.database)

        await self.database.wallets.create(name='cash')
        await self.database.wallets.create(name='credit')
        await self.database.wallets.create(name='debit')


class TestCreateWallet(TestWallet):
    async def test_create_wallet(self):
        wallet = await self.wallets.create(name='credit')

        self.assert_that(wallet['id']).is_not_none()
        self.assert_that(wallet['name']).is_equal_to('credit')

    async def test_error_unexpected_when_creating_wallet(self):
        with patch.object(self.database.wallets, 'create') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntCreateWallet):
                await self.wallets.create(name='credit')


class TestGetWallets(TestWallet):
    async def test_get_wallets(self):
        wallets = await self.wallets.get_list()

        self.assert_that(wallets).is_length(3)

        for wallet in wallets:
            self.assert_that(wallet).contains_only(
                'id', 'name', 'created_at', 'updated_at'
            )

    async def test_error_unexpected_when_getting_wallets(self):
        with patch.object(self.database.wallets, 'find_all') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntGetWallets):
                await self.wallets.get_list()
