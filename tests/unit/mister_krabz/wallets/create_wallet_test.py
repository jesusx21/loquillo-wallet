from unittest.mock import patch
from tests import TestCase

from mister_krabz.wallets import CreateWallet
from mister_krabz.wallets.errors import CouldnCreateWallet


class TestCreateWallet(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()

    async def test_create_wallet(self):
        create_wallet = CreateWallet(self.database, name='credit')

        wallet = await create_wallet.run()

        self.assert_that(wallet.id).is_not_none()
        self.assert_that(wallet.created_at).is_not_none()
        self.assert_that(wallet.created_at).is_not_none()
        self.assert_that(wallet.name).is_equal_to('credit')

    async def test_error_unexpected_when_creating_wallet(self):
        create_wallet = CreateWallet(self.database, name='credit')

        with patch.object(self.database.wallets, 'create') as mock:
            mock.side_effect = Exception()

            with self.assertRaises(CouldnCreateWallet):
                await create_wallet.run()
