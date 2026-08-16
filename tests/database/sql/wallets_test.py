
from unittest.mock import patch
from uuid import UUID, uuid4

from tests.database.sql import SQLTestCase
from tests.database.sql.fixtures import constants, load_fixtures
from tests.database.sql.fixtures.accounts import account_fixtures
from tests.database.sql.fixtures.wallets import wallet_fixtures

from database.stores.errors import DatabaseError, InvalidId, WalletNotFound
from domain.entities.wallet import Wallet, WalletType


class TestWalletsStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()
        await load_fixtures(self.engine, [account_fixtures])


class TestCreateWallet(TestWalletsStore):
    async def async_set_up(self):
        await super().async_set_up()

        self.wallet_to_create = Wallet(
            name='Test Wallet',
            type=WalletType.DEBIT_CARD,
            account_id=constants.ALBO_ACCOUNT_ID
        )

    async def test_create_wallet(self):
        wallet = await self.database.wallets.create(self.wallet_to_create)

        self.assert_that(wallet).is_instance_of(Wallet)
        self.assert_that(wallet.id).is_instance_of(UUID)
        self.assert_that(wallet.name).is_equal_to('Test Wallet')
        self.assert_that(wallet.account_id).is_equal_to(constants.ALBO_ACCOUNT_ID)
        self.assert_that(wallet.type).is_equal_to(WalletType.DEBIT_CARD)

    async def test_error_on_creating_account(self):
        with patch.object(self.database.wallets, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.wallets.create(self.wallet_to_create)


class TestFindWalletById(TestWalletsStore):
    async def async_set_up(self):
        await super().async_set_up()

        await load_fixtures(self.engine, [wallet_fixtures])

    async def test_find_by_id(self):
        wallet = await self.database.wallets.find_by_id(constants.ALBO_WALLET_ID)

        self.assert_that(wallet).is_instance_of(Wallet)
        self.assert_that(wallet.account_id).is_equal_to(constants.ALBO_ACCOUNT_ID)
        self.assert_that(wallet.name).is_equal_to('Albo')
        self.assert_that(wallet.type).is_equal_to(WalletType.DEBIT_CARD)

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
                await self.database.wallets.find_by_id(constants.BBVA_WALLET_ID)
