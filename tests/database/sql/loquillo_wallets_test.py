from uuid import UUID, uuid4

from unittest.mock import patch

from .fixtures import load_fixtures, constants
from tests.database.sql import SQLTestCase

from database.stores.errors import DatabaseError
from domain.entities import LoquilloWallet


class TestLoquilloWalletsStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

        await load_fixtures(self.engine, 'accounts', 'users')


class TestCreateLoquilloWallet(TestLoquilloWalletsStore):
    async def async_set_up(self):
        await super().async_set_up()

        self.loquillo_wallet = LoquilloWallet(
            user_id=constants.USER_ID,
            incomes_account_id=constants.HSBC_ACCOUNT_ID,
            expenses_account_id=constants.STORI_ACCOUNT_ID
        )

    async def test_create_loquillo_wallet(self):
        created = await self.database.loquillo_wallets.create(self.loquillo_wallet)

        self.assert_that(created).is_instance_of(LoquilloWallet)
        self.assert_that(created.id).is_instance_of(UUID)
        self.assert_that(created.user_id).is_equal_to(constants.USER_ID)
        self.assert_that(created.incomes_account_id).is_equal_to(constants.HSBC_ACCOUNT_ID)
        self.assert_that(created.expenses_account_id).is_equal_to(constants.STORI_ACCOUNT_ID)

    async def test_error_on_creating_loquillo_wallet(self):
        with patch.object(self.database.loquillo_wallets, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.loquillo_wallets.create(self.loquillo_wallet)


class TestFindLoquilloWalletByUserId(TestLoquilloWalletsStore):
    async def async_set_up(self):
        await super().async_set_up()

        await load_fixtures(self.engine, 'loquillo_wallets')

    async def test_find_by_user_id(self):
        loquillo_wallet = await self.database.loquillo_wallets.find_by_user_id(constants.USER_ID)

        self.assert_that(loquillo_wallet).is_instance_of(LoquilloWallet)
        self.assert_that(loquillo_wallet.user_id).is_equal_to(constants.USER_ID)
        self.assert_that(loquillo_wallet.incomes_account_id).is_equal_to(constants.ALBO_ACCOUNT_ID)
        self.assert_that(loquillo_wallet.expenses_account_id).is_equal_to(constants.BBVA_ACCOUNT_ID)

    async def test_raise_error_when_user_has_no_loquillo_wallet(self):
        with self.assertRaises(DatabaseError):
            await self.database.loquillo_wallets.find_by_user_id(uuid4())
