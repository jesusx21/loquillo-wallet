from uuid import uuid4

from unittest.mock import patch

from tests import TestCase
from tests.unit.domain.fixtures import load_fixtures, constants

from domain.entities import Account, Wallet
from domain.entities.wallet import WalletType
from domain.crud.wallets import Wallets
from domain.crud.wallets.errors import (
  WalletNotFound,
  CouldNotCreateWallet,
  CouldNotGetWallet,
  CouldNotGetWallets
)


class TestWalletsCRUD(TestCase):
    def set_up(self):
        self.database = self.get_database()
        self.wallets = Wallets(self.database)
        self.user_id = uuid4()


class TestCreateWallet(TestWalletsCRUD):
    async def test_create_wallet(self):
        wallet = await self.wallets.create('Efectivo')

        self.assert_that(wallet).is_instance_of(Wallet)
        self.assert_that(wallet.id).is_not_none()
        self.assert_that(wallet.created_at).is_not_none()
        self.assert_that(wallet.updated_at).is_not_none()
        self.assert_that(wallet.name).is_equal_to('Efectivo')
        self.assert_that(wallet.user_id).is_equal_to(self.user_id)

    async def test_create_account_when_creating_a_wallet(self):
        wallet = await self.wallets.create('Efectivo')
        account = await self.database.accounts.find_by_id(wallet.account_id)

        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.id).is_not_none()
        self.assert_that(account.name).is_equal_to('Cuenta de Efectivo')

    async def test_error_unexpected_when_creating_wallet(self):
        with patch.object(self.database.wallets, 'create') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldNotCreateWallet):
                await self.wallets.create('Efectivo')


class TestGetWalletById(TestWalletsCRUD):
    async def async_set_up(self):
        await super().async_set_up()

        self.wallet = await self.wallets.create('Efectivo')

    async def test_get_wallet_by_id(self):
        wallet = await self.wallets.get_by_id(self.wallet.id)

        self.assert_that(wallet).is_not_none()
        self.assert_that(wallet).is_instance_of(Wallet)
        self.assert_that(wallet.id).is_equal_to(self.wallet.id)
        self.assert_that(wallet.name).is_equal_to('Efectivo')
        self.assert_that(wallet.user_id).is_equal_to(self.user_id)
        self.assert_that(wallet.created_at).is_equal_to(self.wallet.created_at)
        self.assert_that(wallet.updated_at).is_equal_to(self.wallet.updated_at)

    async def test_raise_error_when_wallet_not_found(self):
        with self.assertRaises(WalletNotFound):
            await self.wallets.get_by_id(uuid4())

    async def test_raise_error_when_database_fails(self):
        with patch.object(self.database.wallets, 'find_by_id') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotGetWallet):
                await self.wallets.get_by_id(self.wallet.id)


class TestGetWalletsByTypes(TestWalletsCRUD):
    async def async_set_up(self):
        await super().async_set_up()

        await load_fixtures(self.database, ['accounts', 'wallets'])
        self.user_id = constants.FIRST_USER_ID

    async def test_get_same_type_wallets(self):
        wallets = await self.wallets.get_by_types(self.user_id, [WalletType.DEBIT_CARD])

        self.assert_that(wallets).is_length(2)

        for wallet in wallets:
            self.assert_that(wallet.type.value).is_equal_to('debit_card')
            self.assert_that(wallet.user_id).is_equal_to(constants.FIRST_USER_ID)

    async def test_get_wallets_for_multiple_types(self):
        wallets = await self.wallets.get_by_types(
            self.user_id,
            [WalletType.DEBIT_CARD, WalletType.CASH]
        )

        self.assert_that(wallets).is_length(4)

        for wallet in wallets:
            self.assert_that(wallet.type.value).is_in('debit_card', 'cash')
            self.assert_that(wallet.user_id).is_equal_to(constants.FIRST_USER_ID)

    async def test_get_wallets_for_all_types(self):
        wallets = await self.wallets.get_by_types(
            self.user_id,
            [WalletType.DEBIT_CARD, WalletType.CASH, WalletType.CREDIT_CARD]
        )

        self.assert_that(wallets).is_length(5)

        for wallet in wallets:
            self.assert_that(wallet.user_id).is_equal_to(constants.FIRST_USER_ID)
            self.assert_that(wallet.type.value).is_in('debit_card', 'cash', 'credit_card')

    async def test_get_wallets_return_empty_when_types_is_empty(self):
        wallets = await self.wallets.get_by_types(self.user_id, [])

        self.assert_that(wallets).is_equal_to([])

    async def test_get_wallets_returns_empty_list_when_no_wallet_matches(self):
        wallets = await self.wallets.get_by_types(
            constants.SECOND_USER_ID,
            [WalletType.DEBIT_CARD, WalletType.CASH, WalletType.CREDIT_CARD]
        )

        self.assert_that(wallets).is_equal_to([])

    async def test_raises_could_not_get_wallets_when_database_fails(self):
        with patch.object(self.database.wallets, 'find') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotGetWallets):
                await self.wallets.get_by_types(self.user_id, [WalletType.DEBIT_CARD])
