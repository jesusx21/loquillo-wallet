from tests import TestCase
from unittest.mock import patch

from domain.entities import Account
from domain.entities.wallet import WalletType
from domain.errors import CouldNotCreateAccount, CouldNotCreateWallet
from domain.use_cases import CreateWallet


class TestCreateWallet(TestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

        self.create_wallet = CreateWallet(self.database, 'Efectivo', WalletType.CASH)

    async def test_create_wallet(self):
        wallet = await self.create_wallet.execute()

        self.assert_that(wallet.id).is_not_none()
        self.assert_that(wallet.created_at).is_not_none()
        self.assert_that(wallet.updated_at).is_not_none()
        self.assert_that(wallet.name).is_equal_to('Efectivo')

    async def test_create_account_when_creating_a_wallet(self):
        wallet = await self.create_wallet.execute()
        account = await self.database.accounts.find_by_id(wallet.account_id)

        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.id).is_not_none()
        self.assert_that(account.name).is_equal_to('Efectivo Account')

    async def test_error_unexpected_when_creating_account(self):
        with patch.object(self.database.accounts, 'create') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldNotCreateAccount):
                await self.create_wallet.execute()

    async def test_error_unexpected_when_creating_wallet(self):
        with patch.object(self.database.wallets, 'create') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldNotCreateWallet):
                await self.create_wallet.execute()
