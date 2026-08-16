from uuid import UUID, uuid4

from unittest.mock import patch

from . import SQLTestCase
from .fixtures import load_fixtures
from .fixtures.accounts import account_fixtures
from .fixtures import constants

from database.stores.errors import AccountNotFound, DatabaseError, InvalidId
from domain.entities.account import Account, AccountType
from domain.entities.detail_account import DetailAccount


class TestAccountsStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

    async def async_tear_down(self):
        await super().async_tear_down()


class TestCreateAccount(TestAccountsStore):
    async def test_create_detail_account(self):
        account_to_create = Account(
            name='Test Detail Account',
            type=AccountType.DETAIL
        )

        account = await self.database.accounts.create(account_to_create)

        self.assert_that(account).is_instance_of(DetailAccount)
        self.assert_that(account.id).is_instance_of(UUID)
        self.assert_that(account.name).is_equal_to('Test Detail Account')
        self.assert_that(account.type).is_equal_to(AccountType.DETAIL)
        self.assert_that(account.created_at).is_not_none()
        self.assert_that(account.updated_at).is_not_none()

    async def test_create_summary_account(self):
        account_to_create = Account(
            name='Test Summary Account',
            type=AccountType.SUMMARY
        )

        account = await self.database.accounts.create(account_to_create)

        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.id).is_instance_of(UUID)
        self.assert_that(account.name).is_equal_to('Test Summary Account')
        self.assert_that(account.type).is_equal_to(AccountType.SUMMARY)
        self.assert_that(account.created_at).is_not_none()
        self.assert_that(account.updated_at).is_not_none()

    async def test_error_on_creating_account(self):
        account_to_create = Account(
            name='Test Detail Account',
            type=AccountType.DETAIL
        )

        with patch.object(self.database.accounts, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.accounts.create(account_to_create)


class TestFindAccountById(TestAccountsStore):
    async def async_set_up(self):
        await super().async_set_up()

        await load_fixtures(self.engine, [account_fixtures])

    async def test_find_by_id(self):
        account = await self.database.accounts.find_by_id(constants.ACCOUNT_ID)

        self.assert_that(account).is_instance_of(DetailAccount)
        self.assert_that(account.id).is_equal_to(constants.ACCOUNT_ID)
        self.assert_that(account.name).is_equal_to('Credit Card Account')

    async def test_raise_error_when_account_does_not_exist(self):
        with self.assertRaises(AccountNotFound):
            await self.database.accounts.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.accounts.find_by_id('invalid-id')

    async def test_raise_error_on_finding_account_by_id(self):
        with patch.object(self.database.accounts, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.accounts.find_by_id(constants.ACCOUNT_ID)
