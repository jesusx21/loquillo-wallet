from uuid import uuid4

from unittest.mock import patch

from tests import TestCase

from domain.entities import Account
from domain.crud.accounts import Accounts
from domain.crud.accounts.errors import (
  AccountNotFound,
  CouldNotCreateAccount,
  CouldNotGetAccount
)


class TestAccountsCRUD(TestCase):
    def set_up(self):
        self.database = self.get_database()
        self.accounts = Accounts(self.database)


class TestCreateAccount(TestAccountsCRUD):
    async def test_create_account(self):
        account = await self.accounts.create('Debt Account')

        self.assert_that(account).is_not_none()
        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.name).is_equal_to('Debt Account')
        self.assert_that(account.type.value).is_equal_to('detail')
        self.assert_that(account.id).is_not_none()
        self.assert_that(account.created_at).is_not_none()
        self.assert_that(account.updated_at).is_not_none()

    async def test_raise_error_when_database_fails(self):
        with patch.object(self.database.accounts, 'create') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotCreateAccount):
                await self.accounts.create('Debt Account')


class TestGetAccountById(TestAccountsCRUD):
    async def async_set_up(self):
        await super().async_set_up()

        self.account = await self.accounts.create_income_account('Income Account')

    async def test_get_account_by_id(self):
        account = await self.accounts.get_account_by_id(self.account.id)

        self.assert_that(account).is_not_none()
        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.id).is_equal_to(self.account.id)
        self.assert_that(account.name).is_equal_to('Income Account')
        self.assert_that(account.type.value).is_equal_to('detail')
        self.assert_that(account.created_at).is_equal_to(self.account.created_at)
        self.assert_that(account.updated_at).is_equal_to(self.account.updated_at)

    async def test_raise_error_when_account_not_found(self):
        with self.assertRaises(AccountNotFound):
            await self.accounts.get_account_by_id(uuid4())

    async def test_raise_error_when_database_fails(self):
        with patch.object(self.database.accounts, 'find_by_id') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotGetAccount):
                await self.accounts.get_account_by_id(self.account.id)
