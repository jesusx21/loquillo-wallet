from uuid import uuid4

from unittest.mock import patch
from tests.database import TestCase

from database.stores.errors import DatabaseError, InvalidId, WalletNotFound


class TestWalletsStore(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()


class TestCreateWallet(TestWalletsStore):
    async def test_create_wallet(self):
        wallet = await self.database.wallets.create(name='cash')

        self.assert_that(wallet['id']).is_not_none()
        self.assert_that(wallet['name']).is_equal_to('cash')

    async def test_error_on_creating_wallet(self):
        with patch.object(self.database.wallets, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.wallets.create(name='cash')


class TestFindWalletById(TestWalletsStore):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.wallet = await self.database.wallets.create(name='cash')

    async def test_find_by_id(self):
        wallet = await self.database.wallets.find_by_id(self.wallet['id'])

        self.assert_that(wallet['id']).is_equal_to(self.wallet['id'])
        self.assert_that(wallet['name']).is_equal_to(self.wallet['name'])
        self.assert_that(wallet['created_at']).is_equal_to(self.wallet['created_at'])
        self.assert_that(wallet['updated_at']).is_equal_to(self.wallet['updated_at'])

    async def test_raise_error_when_wallet_does_not_exist(self):
        with self.assertRaises(WalletNotFound):
            await self.database.wallets.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.wallets.find_by_id('invalid-id')

    async def test_raise_error_on_finding_wallet_by_id(self):
        with patch.object(self.database.wallets, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.wallets.find_by_id(self.wallet['id'])
