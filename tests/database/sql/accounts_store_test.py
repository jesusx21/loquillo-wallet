from uuid import uuid4

from unittest.mock import patch
from mister_krabz.entities.account import Account
from tests.database import TestCase

from database.stores.errors import AccountNotFound, DatabaseError, InvalidId


class TestAccountsStore(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()
        self.account = await self.create_account(self.database, name='Cash')

        await self.create_account(self.database, name='Credit')
        await self.create_account(self.database, name='Debts')
        await self.create_account(self.database, name='Loans')
        await self.create_account(self.database, name='Savings')


class TestCreateAccount(TestAccountsStore):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.account = Account(name='Transactions')

    async def test_create_account(self):
        account = await self.database.accounts.create(self.account)

        self.assert_that(account.id).is_not_none()
        self.assert_that(account.name).is_equal_to('Transactions')
        self.assert_that(account.created_at).is_not_none()
        self.assert_that(account.updated_at).is_not_none()

    async def test_error_on_creating_account(self):
        with patch.object(self.database.accounts, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.accounts.create(self.account)


class TestUpdateAccount(TestAccountsStore):
    async def test_update_account(self):
        self.account.name = 'Loans'

        account = await self.database.accounts.update(self.account)

        self.assert_that(account.id).is_equal_to(self.account.id)
        self.assert_that(account.name).is_equal_to('Loans')

    async def test_error_on_missing_id(self):
        self.account.id = None

        with self.assertRaises(InvalidId):
            await self.database.accounts.update(self.account)

    async def test_error_on_invalid_id(self):
        self.account.id = 'invalid_id'

        with self.assertRaises(InvalidId):
            await self.database.accounts.update(self.account)

    async def test_error_on_account_not_found(self):
        self.account.id = uuid4()

        with self.assertRaises(AccountNotFound):
            await self.database.accounts.update(self.account)


class TestFindAccountById(TestAccountsStore):
    async def test_find_by_id(self):
        account = await self.database.accounts.find_by_id(self.account.id)

        self.assert_that(account.id).is_equal_to(self.account.id)
        self.assert_that(account.name).is_equal_to(self.account.name)
        self.assert_that(account.created_at).is_equal_to(self.account.created_at)
        self.assert_that(account.updated_at).is_equal_to(self.account.updated_at)

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
                await self.database.accounts.find_by_id(self.account.id)
