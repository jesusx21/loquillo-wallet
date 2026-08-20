
from unittest.mock import patch
from uuid import UUID, uuid4

from tests.database.sql import SQLTestCase
from tests.database.sql.fixtures import constants, load_fixtures

from database.stores.errors import DatabaseError, InvalidId, WalletNotFound
from domain.entities.wallet import Wallet, WalletType


class TestWalletsStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()
        await load_fixtures(self.engine, 'accounts', 'users', 'wallets')


class TestCreateWallet(TestWalletsStore):
    async def async_set_up(self):
        await super().async_set_up()

        self.wallet_to_create = Wallet(
            name='Test Wallet',
            type=WalletType.DEBIT_CARD,
            account_id=constants.ALBO_ACCOUNT_ID,
            user_id=constants.SECOND_USER_ID
        )

    async def test_create_wallet(self):
        wallet = await self.database.wallets.create(self.wallet_to_create)

        self.assert_that(wallet).is_instance_of(Wallet)
        self.assert_that(wallet.id).is_instance_of(UUID)
        self.assert_that(wallet.name).is_equal_to('Test Wallet')
        self.assert_that(wallet.account_id).is_equal_to(constants.ALBO_ACCOUNT_ID)
        self.assert_that(wallet.type).is_equal_to(WalletType.DEBIT_CARD)
        self.assert_that(wallet.user_id).is_equal_to(constants.SECOND_USER_ID)

    async def test_error_on_creating_account(self):
        with patch.object(self.database.wallets, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.wallets.create(self.wallet_to_create)


class TestFindWalletById(TestWalletsStore):
    async def test_find_by_id(self):
        wallet = await self.database.wallets.find_by_id(constants.ALBO_WALLET_ID)

        self.assert_that(wallet).is_instance_of(Wallet)
        self.assert_that(wallet.account_id).is_equal_to(constants.ALBO_ACCOUNT_ID)
        self.assert_that(wallet.name).is_equal_to('Albo')
        self.assert_that(wallet.type).is_equal_to(WalletType.DEBIT_CARD)
        self.assert_that(wallet.user_id).is_equal_to(constants.USER_ID)

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


class TestFindWalletsByType(TestWalletsStore):
    async def test_find_wallets_for_user_and_multiple_types(self):
        wallets = await self.database.wallets.find(
            user_id=constants.USER_ID,
            type=[WalletType.DEBIT_CARD, WalletType.CREDIT_CARD]
        )

        self.assert_that(wallets).is_length(2)
        self.assert_that({wallet.type for wallet in wallets}).is_equal_to({
            WalletType.CREDIT_CARD,
            WalletType.DEBIT_CARD,
        })

    async def test_find_wallets_for_user_and_single_type(self):
        wallets = await self.database.wallets.find(
            user_id=constants.USER_ID,
            type=WalletType.CREDIT_CARD
        )

        self.assert_that(wallets).is_length(1)
        self.assert_that(wallets[0].name).is_equal_to('Stori')
