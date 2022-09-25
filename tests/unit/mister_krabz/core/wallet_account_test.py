from uuid import uuid4
from mister_krabz.core.wallet_account import CouldNotGetAccount, WalletAccount
from tests import TestCase


class TestWalletAccount(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()
        self.account = await self.create_account(self.database, name='Cash Transaction')
        self.wallet = await self.create_account(self.database, name='Cash')
    

class TestGetAccount(TestWalletAccount):
    async def test_get_account(self):
        wallet_account = WalletAccount(self.database, self.wallet, self.account.id)
        
        account = await wallet_account.get_account()
        self.assert_that(account.id).is_equal_to(self.account.id)
        self.assert_that(account.name).is_equal_to(self.account.name)
        self.assert_that(account.created_at).is_equal_to(self.account.created_at)
        self.assert_that(account.updated_at).is_equal_to(self.account.updated_at)

    async def test_return_error_when_account_does_not_exist(self):
        wallet_account = WalletAccount(self.database, self.wallet, uuid4())

        with self.assertRaises(CouldNotGetAccount):
            await wallet_account.get_account()

    async def test_return_error_when_account_id_is_invalid(self):
        wallet_account = WalletAccount(self.database, self.wallet, 'uuid4(')

        with self.assertRaises(CouldNotGetAccount):
            await wallet_account.get_account()

    async def test_return_error_when_account_id_is_null(self):
        wallet_account = WalletAccount(self.database, self.wallet, None)

        with self.assertRaises(CouldNotGetAccount):
            await wallet_account.get_account()