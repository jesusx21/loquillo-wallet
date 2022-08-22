from unittest.mock import patch
from uuid import uuid4
from tests import TestCase

from mister_krabz import Wallets
from mister_krabz.errors import (
    CouldntCreateWallet,
    CouldntGetWallets,
    CouldntUpdateWallets,
    WalletNotFound
)


class TestWallet(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()
        self.wallets = Wallets(self.database)

        self.wallet = await self.create_wallet(self.database, name='cash')
        await self.create_wallet(self.database, name='cash')
        await self.create_wallet(self.database, name='credit')
        await self.create_wallet(self.database, name='debit')


class TestCreateWallet(TestWallet):
    async def test_create_wallet(self):
        wallet = await self.wallets.create(name='credit')

        self.assert_that(wallet.id).is_not_none()
        self.assert_that(wallet.created_at).is_not_none()
        self.assert_that(wallet.updated_at).is_not_none()
        self.assert_that(wallet.name).is_equal_to('credit')

    async def test_create_account_when_creating_a_wallet(self):
        wallet = await self.wallets.create(name='credit')
        accounts = await self.database.accounts.find_by_wallet_id(wallet['id'])
        account = accounts[0]

        self.assert_that(accounts).is_length(1)
        self.assert_that(account['id']).is_not_none()
        self.assert_that(account['wallet_id']).is_equal_to(wallet['id'])
        self.assert_that(account['name']).is_equal_to('Transactions')

    async def test_error_unexpected_when_creating_wallet(self):
        with patch.object(self.database.wallets, 'create') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntCreateWallet):
                await self.wallets.create(name='credit')


class TestUpdateWallet(TestWallet):
    async def test_update_wallet(self):
        wallet = await self.wallets.update(self.wallet.id, name='Another Name')

        self.assert_that(wallet.id).is_equal_to(self.wallet.id)
        self.assert_that(wallet.name).is_equal_to('Another Name')

    async def test_error_on_unexistent_wallet(self):
        with self.assertRaises(WalletNotFound):
            await self.wallets.update(uuid4(), name='Another Name')

    async def test_error_unexpected_when_creating_wallet(self):
        with patch.object(self.database.wallets, 'update') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntUpdateWallets):
                await self.wallets.update(self.wallet.id, 'Another Name')


class TestGetWalletById(TestWallet):
    async def test_get_wallet_by_id(self):
        wallet = await self.wallets.get_by_id(self.wallet.id)

        self.assert_that(wallet.id).is_equal_to(self.wallet.id)
        self.assert_that(wallet.name).is_equal_to(self.wallet.name)

    async def test_error_on_unexistent_wallet(self):
        with self.assertRaises(WalletNotFound):
            await self.wallets.get_by_id(uuid4())

    async def test_error_unexpected_when_creating_wallet(self):
        with patch.object(self.database.wallets, 'find_by_id') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntGetWallets):
                await self.wallets.get_by_id(self.wallet.id)


class TestGetWallets(TestWallet):
    async def test_get_wallets(self):
        wallets = await self.wallets.get_list()

        self.assert_that(wallets).is_length(4)

    async def test_error_unexpected_when_getting_wallets(self):
        with patch.object(self.database.wallets, 'find_all') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntGetWallets):
                await self.wallets.get_list()
