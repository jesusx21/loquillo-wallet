from uuid import uuid4

from unittest.mock import patch
from mister_krabz.entities import Wallet
from tests.database import TestCase

from database.stores.errors import DatabaseError, InvalidId, WalletNotFound


class TestWalletsStore(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()
        self.wallet = await self.create_wallet(self.database, name='cash')

        await self.create_wallet(self.database, name='debit')
        await self.create_wallet(self.database, name='credit')
        await self.create_wallet(self.database, name='loans')
        await self.create_wallet(self.database, name='debts')


class TestCreateWallet(TestWalletsStore):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        account = await self.create_account(self.database, 'Cash')
        self.wallet = Wallet(name='cash', account=account)

    async def test_create_wallet(self):
        wallet = await self.database.wallets.create(self.wallet)

        self.assert_that(wallet.id).is_not_none()
        self.assert_that(wallet.created_at).is_not_none()
        self.assert_that(wallet.updated_at).is_not_none()
        self.assert_that(wallet.name).is_equal_to(self.wallet.name)

    async def test_error_on_creating_wallet(self):
        with patch.object(self.database.wallets, '_execute') as mock:
            mock.side_effect = Exception()

            with self.assertRaises(DatabaseError):
                await self.database.wallets.create(self.wallet)

class TestUpdateWallet(TestWalletsStore):
    async def test_update_wallet(self):
        self.wallet.name = 'Name Updated'

        wallet = await self.database.wallets.update(self.wallet)

        self.assert_that(wallet.id).is_equal_to(self.wallet.id)
        self.assert_that(wallet.name).is_equal_to(self.wallet.name)
        self.assert_that(wallet.created_at).is_equal_to(self.wallet.created_at)
        self.assert_that(wallet.updated_at).is_not_equal_to(self.wallet.updated_at)

    async def test_error_on_missing_id(self):
        self.wallet.id = None

        with self.assertRaises(InvalidId):
            await self.database.wallets.update(self.wallet)

    async def test_error_on_invalid_id(self):
        self.wallet.id = 'invalid_id'

        with self.assertRaises(InvalidId):
            await self.database.wallets.update(self.wallet)

    async def test_error_on_wallet_not_found(self):
        self.wallet.id = uuid4()

        with self.assertRaises(WalletNotFound):
            await self.database.wallets.update(self.wallet)

class TestFindWalletById(TestWalletsStore):
    async def test_find_by_id(self):
        wallet = await self.database.wallets.find_by_id(self.wallet.id)

        self.assert_that(wallet.id).is_equal_to(self.wallet.id)
        self.assert_that(wallet.name).is_equal_to(self.wallet.name)
        self.assert_that(wallet.created_at).is_equal_to(self.wallet.created_at)
        self.assert_that(wallet.updated_at).is_equal_to(self.wallet.updated_at)

    async def test_raise_error_when_wallet_does_not_exist(self):
        with self.assertRaises(WalletNotFound):
            await self.database.wallets.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.wallets.find_by_id('invalid-id')

    async def test_raise_error_on_finding_wallet_by_id(self):
        with patch.object(self.database.wallets._store, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.wallets.find_by_id(self.wallet.id)


class TestFindAllWallets(TestWalletsStore):
    async def test_find_all_wallets(self):
        wallets = await self.database.wallets.find_all()

        self.assert_that(wallets).is_length(5)

    async def test_raise_error_on_finding_wallets(self):
        with patch.object(self.database.wallets._store, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.wallets.find_all()
