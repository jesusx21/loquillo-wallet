from unittest.mock import patch
from tests import TestCase

from mister_krabz.wallets import GetWallets
from mister_krabz.wallets.errors import CouldnGetWallets


class TestGetWallets(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()

        await self.database.wallets.create(name='cash')
        await self.database.wallets.create(name='credit')
        await self.database.wallets.create(name='debit')

    async def test_get_wallets(self):
        get_wallets = GetWallets(self.database)

        wallets = await get_wallets.run()

        self.assert_that(wallets).is_length(3)

        for wallet in wallets:
            self.assert_that(wallet).contains_only(
                'id', 'name', 'created_at', 'updated_at'
            )

    async def test_error_unexpected_when_getting_wallets(self):
        get_wallets = GetWallets(self.database)

        with patch.object(self.database.wallets, 'find_all') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldnGetWallets):
                await get_wallets.run()
