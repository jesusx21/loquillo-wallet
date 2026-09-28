from tests import TestCase

from unittest.mock import patch

from tests.unit.domain.fixtures import load_fixtures, constants

from domain.crud.transactions import Transactions
from domain.crud.transactions.errors import CouldNotCreateTransaction
from domain.entities.transaction import Transaction, TransactionStatus


class TestTransactionsCRUD(TestCase):
    async def async_set_up(self):
        self.database = self.get_database()

        self.transactions = Transactions(self.database)

        await load_fixtures(self.database, ['accounts'])


class TestCreateTransactions(TestTransactionsCRUD):
    async def test_create_transaction(self):
        transaction = await self.transactions.create(
            source_account_id=constants.BBVA_ACCOUNT_ID,
            source_concept='Transfer to Scotiabank',
            target_account_id=constants.SCOTIABANK_ACCOUNT_ID,
            target_concept='Transfer from BBVA',
            amount=25_000_15,
            note='Transfer'
        )

        self.assert_that(transaction).is_instance_of(Transaction)
        self.assert_that(transaction.status).is_equal_to(TransactionStatus.COMPLETED)
        self.assert_that(transaction.note).is_equal_to('Transfer')
        self.assert_that(transaction.date).is_not_none()

        self.assert_that(transaction.is_balanced()).is_true()

        self.assert_that(transaction.source_entry.amount).is_equal_to(-25_000_15)
        self.assert_that(transaction.source_entry.concept) \
            .is_equal_to('Transfer to Scotiabank')
        self.assert_that(transaction.source_entry.account_id) \
            .is_equal_to(constants.BBVA_ACCOUNT_ID)

        self.assert_that(transaction.target_entry.amount).is_equal_to(25_000_15)
        self.assert_that(transaction.target_entry.concept) \
            .is_equal_to('Transfer from BBVA')
        self.assert_that(transaction.target_entry.account_id) \
            .is_equal_to(constants.SCOTIABANK_ACCOUNT_ID)

    async def test_raises_could_not_create_transaction_when_database_fails(self):
        with patch.object(self.database.transactions, 'create') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotCreateTransaction):
                await self.transactions.create(
                    source_account_id=constants.BBVA_ACCOUNT_ID,
                    source_concept='Transfer to Scotiabank',
                    target_account_id=constants.SCOTIABANK_ACCOUNT_ID,
                    target_concept='Transfer from BBVA',
                    amount=25_000_15,
                    note='Transfer'
                )
