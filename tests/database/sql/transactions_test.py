from uuid import UUID, uuid4

from unittest.mock import patch

from . import SQLTestCase
from .fixtures import load_fixtures
from .fixtures import constants
from .fixtures.transactions import transaction_fixtures

from database.stores.errors import DatabaseError, InvalidId, TransactionNotFound
from domain.entities.transaction import Transaction, TransactionStatus


class TestTransactionsStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

    async def async_tear_down(self):
        await super().async_tear_down()


class TestCreateTransaction(TestTransactionsStore):
    async def test_create_transaction(self):
        transaction_to_create = Transaction(
            description='Test transaction',
            status=TransactionStatus.PENDING
        )

        transaction = await self.database.transactions.create(transaction_to_create)

        self.assert_that(transaction).is_instance_of(Transaction)
        self.assert_that(transaction.id).is_instance_of(UUID)
        self.assert_that(transaction.description).is_equal_to('Test transaction')
        self.assert_that(transaction.status).is_equal_to(TransactionStatus.PENDING)
        self.assert_that(transaction.created_at).is_not_none()

    async def test_error_on_creating_transaction(self):
        transaction_to_create = Transaction(
            description='Test transaction',
            status=TransactionStatus.PENDING
        )

        with patch.object(self.database.transactions, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.transactions.create(transaction_to_create)


class TestFindTransactionById(TestTransactionsStore):
    async def async_set_up(self):
        await super().async_set_up()

        await load_fixtures(self.engine, [transaction_fixtures])

    async def test_find_by_id(self):
        transaction = await self.database.transactions.find_by_id(constants.TRANSACTION_ID)

        self.assert_that(transaction).is_instance_of(Transaction)
        self.assert_that(transaction.id).is_equal_to(constants.TRANSACTION_ID)
        self.assert_that(transaction.description).is_equal_to('Initial transaction')
        self.assert_that(transaction.status).is_equal_to(TransactionStatus.COMPLETED)

    async def test_raise_error_when_transaction_does_not_exist(self):
        with self.assertRaises(TransactionNotFound):
            await self.database.transactions.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.transactions.find_by_id('invalid-id')

    async def test_raise_error_on_finding_transaction_by_id(self):
        with patch.object(self.database.transactions, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.transactions.find_by_id(constants.TRANSACTION_ID)
