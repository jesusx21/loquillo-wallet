from uuid import uuid4
from mister_krabz.core.wallet_account import WalletAccount
from mister_krabz.entities.wallet import PrivateField, Wallet, WalletAccountAlreadySet, WalletAccountNotSet
from tests import TestCase


class TestWallet(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.wallet = Wallet(name='Cash')
        self.db = self.get_database()
    
    def test_wallet_account_raises_error(self):
        with self.assertRaises(PrivateField):
            self.wallet.wallet_account
    
    def test_set_wallet_account(self):
        self.wallet.wallet_account = WalletAccount(self.db, self.wallet, uuid4())

        self.assert_that(self.wallet._wallet_account).is_not_none()
    
    def test_error_when_setting_wallet_account_already_set(self):
        self.wallet.wallet_account = WalletAccount(self.db, self.wallet, uuid4())

        with self.assertRaises(WalletAccountAlreadySet):
            self.wallet.wallet_account = WalletAccount(self.db, self.wallet, uuid4())
    
    async def test_get_account(self):
        account = await self.create_account(self.db, 'Cash')

        self.wallet.wallet_account = WalletAccount(self.db, self.wallet, account.id)
        account_found = await self.wallet.get_account()

        self.assert_that(account_found.id).is_equal_to(account.id)
    
    async def test_get_account_with_wallet_account_not_set(self):
        with self.assertRaises(WalletAccountNotSet):
            await self.wallet.get_account()

        


