from datetime import datetime
from uuid import UUID

from tests import TestCase
from tests.unit.domain.fixtures import load_fixtures, constants

from domain.crud import CRUD
from domain.use_cases.add_transaction import CategoryNotFound, WalletNotFound
from domain.entities import Transaction, User
from domain.use_cases import AddTransaction
from domain.use_cases.errors import InvalidCategoryType, InvalidTransactionAmount


class TestAddTransaction(TestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()
        self.crud = CRUD(self.database)

        self.user = User(
            id=constants.FIRST_USER_ID,
            names='Jon',
            last_names='Doe',
            email='jon.doe@example.com',
        )

        await load_fixtures(self.database, ['accounts', 'categories', 'wallets'])

    async def test_create_income_transaction(self):
        transaction = await self._create_transaction(
            constants.SANTANDER_WALLET_ID,
            constants.INVERSIONS_CATEGORY_ID,
            100_00
        )

        self.assert_that(transaction).is_instance_of(Transaction)
        self.assert_that(transaction.status.value).is_equal_to('completed')
        self.assert_that(transaction.note).is_none()
        self.assert_that(transaction.date).is_not_none()

        self.assert_that(transaction.is_balanced()).is_true()

        self.assert_that(transaction.source_entry.amount).is_equal_to(-100_00)
        self.assert_that(transaction.source_entry.concept) \
            .is_equal_to('Inversions')
        self.assert_that(transaction.source_entry.account_id) \
            .is_equal_to(constants.INVERSIONS_ACCOUNT_ID)

        self.assert_that(transaction.target_entry.amount).is_equal_to(100_00)
        self.assert_that(transaction.target_entry.concept) \
            .is_equal_to('Inversions')
        self.assert_that(transaction.target_entry.account_id) \
            .is_equal_to(constants.SANTANDER_ACCOUNT_ID)

    async def test_create_expense_transaction(self):
        transaction = await self._create_transaction(
            constants.SANTANDER_WALLET_ID,
            constants.SAVINGS_CATEGORY_ID,
            1_000_00
        )

        self.assert_that(transaction).is_instance_of(Transaction)
        self.assert_that(transaction.status.value).is_equal_to('completed')
        self.assert_that(transaction.note).is_none()
        self.assert_that(transaction.date).is_not_none()

        self.assert_that(transaction.is_balanced()).is_true()

        self.assert_that(transaction.source_entry.amount).is_equal_to(-1_000_00)
        self.assert_that(transaction.source_entry.concept) \
            .is_equal_to('Savings')
        self.assert_that(transaction.source_entry.account_id) \
            .is_equal_to(constants.SANTANDER_ACCOUNT_ID)

        self.assert_that(transaction.target_entry.amount).is_equal_to(1_000_00)
        self.assert_that(transaction.target_entry.concept) \
            .is_equal_to('Savings')
        self.assert_that(transaction.target_entry.account_id) \
            .is_equal_to(constants.SAVINGS_ACCOUNT_ID)

    async def test_create_transaction_with_custom_date(self):
        transaction_date = datetime.now()

        transaction = await self._create_transaction(
            constants.SANTANDER_WALLET_ID,
            constants.INVERSIONS_CATEGORY_ID,
            1_000_00,
            date=transaction_date
        )

        self.assert_that(transaction).is_instance_of(Transaction)
        self.assert_that(transaction.status.value).is_equal_to('completed')
        self.assert_that(transaction.note).is_none()
        self.assert_that(transaction.date).is_equal_to(transaction_date)

    async def test_create_transaction_with_notes(self):
        transaction = await self._create_transaction(
            constants.SANTANDER_WALLET_ID,
            constants.INVERSIONS_CATEGORY_ID,
            1_000_00,
            note='Test note'
        )

        self.assert_that(transaction).is_instance_of(Transaction)
        self.assert_that(transaction.status.value).is_equal_to('completed')
        self.assert_that(transaction.note).is_equal_to('Test note')
        self.assert_that(transaction.date).is_not_none()

    async def test_raise_error_when_category_belongs_to_different_user(self):
        with self.assertRaises(CategoryNotFound):
            await self._create_transaction(
                constants.SANTANDER_WALLET_ID,
                constants.PAYMENTS_ACCOUNT_ID,
                1_000_00
            )

    async def test_raise_error_when_wallet_belongs_to_different_user(self):
        with self.assertRaises(WalletNotFound):
            await self._create_transaction(
                constants.NU_BANK_WALLET_ID,
                constants.INVERSIONS_CATEGORY_ID,
                1_000_00
            )

    async def test_raise_error_on_negative_amount(self):
        with self.assertRaises(InvalidTransactionAmount):
            await self._create_transaction(
                constants.SANTANDER_WALLET_ID,
                constants.INVERSIONS_CATEGORY_ID,
                -1_000_00
            )

    async def test_raise_error_on_zero_amount(self):
        with self.assertRaises(InvalidTransactionAmount):
            await self._create_transaction(
                constants.SANTANDER_WALLET_ID,
                constants.INVERSIONS_CATEGORY_ID,
                0
            )

    async def test_raise_error_on_invalid_category_for_transaction(self):
        with self.assertRaises(InvalidCategoryType):
            await self._create_transaction(
                constants.SANTANDER_WALLET_ID,
                constants.DEBT_CATEGORY_ID,
                100_00
            )

    async def _create_transaction(
        self,
        wallet_id: UUID,
        category_id: UUID,
        amount: int,
        date: datetime = None,
        note: str = None
    ):
        add_transaction = AddTransaction(
            self.crud,
            self.user,
            wallet_id,
            category_id,
            amount,
            date,
            note
        )

        return await add_transaction.execute()
