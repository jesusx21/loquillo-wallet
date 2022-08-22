from uuid import uuid4

from unittest.mock import patch
from tests.database import TestCase

from database.stores.errors import AccountNotFound, DatabaseError, InvalidId


class TestAccountsStore(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()
        self.wallet = await self.database.wallets.create(name='cash')
        self.second_wallet = await self.database.wallets.create(name='debit')
        self.wallet_without_accounts = await self.database.wallets.create(name='credit')
        self.account = await self.database.accounts.create(name='Transactions', wallet=self.wallet)

        await self.database.accounts.create(name='transactions', wallet=self.wallet)
        await self.database.accounts.create(name='debts', wallet=self.wallet)
        await self.database.accounts.create(name='loans', wallet=self.second_wallet)
        await self.database.accounts.create(name='savings', wallet=self.second_wallet)


class TestCreateAccount(TestAccountsStore):
    async def test_create_account(self):
        account = await self.database.accounts.create(name='Transactions', wallet=self.wallet)

        self.assert_that(account['id']).is_not_none()
        self.assert_that(account['name']).is_equal_to('Transactions')
        self.assert_that(account['wallet_id']).is_equal_to(self.wallet['id'])

    async def test_error_on_creating_account(self):
        with patch.object(self.database.accounts._store, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.accounts.create(name='cash', wallet=self.wallet)


class TestUpdateWallet(TestAccountsStore):
    async def test_update_account(self):
        self.account['name'] = 'Loans'

        account = await self.database.accounts.update(self.account)

        self.assert_that(account['id']).is_equal_to(self.account['id'])
        self.assert_that(account['name']).is_equal_to('Loans')

    async def test_error_on_missing_id(self):
        del self.account['id']

        with self.assertRaises(InvalidId):
            await self.database.accounts.update(self.account)

    async def test_error_on_invalid_id(self):
        self.account['id'] = 'invalid_id'

        with self.assertRaises(InvalidId):
            await self.database.accounts.update(self.account)

    async def test_error_on_account_not_found(self):
        self.account['id'] = uuid4()

        with self.assertRaises(AccountNotFound):
            await self.database.accounts.update(self.account)


class TestFindAccountById(TestAccountsStore):
    async def test_find_by_id(self):
        account = await self.database.accounts.find_by_id(self.account['id'])

        self.assert_that(account['id']).is_equal_to(self.account['id'])
        self.assert_that(account['name']).is_equal_to(self.account['name'])
        self.assert_that(account['wallet_id']).is_equal_to(self.account['wallet_id'])
        self.assert_that(account['created_at']).is_equal_to(self.account['created_at'])
        self.assert_that(account['updated_at']).is_equal_to(self.account['updated_at'])

    async def test_raise_error_when_account_does_not_exist(self):
        with self.assertRaises(AccountNotFound):
            await self.database.accounts.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.accounts.find_by_id('invalid-id')

    async def test_raise_error_on_finding_account_by_id(self):
        with patch.object(self.database.accounts._store, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.accounts.find_by_id(self.account['id'])


class TestFindAccountsByWalletId(TestAccountsStore):
    async def test_find_accounts_by_wallet_id(self):
        accounts = await self.database.accounts.find_by_wallet_id(self.wallet['id'])

        self.assert_that(accounts).is_length(3)

        for account in accounts:
            self.assert_that(account['wallet_id']).is_equal_to(self.wallet['id'])
            self.assert_that(account).contains_only(
                'id', 'name', 'wallet_id', 'created_at', 'updated_at'
            )

    async def test_return_empty_list_when_wallet_has_not_accounts(self):
        accounts = await self.database \
            .accounts \
            .find_by_wallet_id(self.wallet_without_accounts['id'])

        self.assert_that(accounts).is_length(0)

    async def test_raise_error_on_finding_accounts_by_wallet_id(self):
        with patch.object(self.database.accounts._store, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.accounts.find_by_wallet_id(self.wallet['id'])
