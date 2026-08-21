from uuid import UUID, uuid4

from unittest.mock import patch

from tests import TestCase
from tests.unit.domain.use_cases.fixtures import load_fixtures, constants

from domain.entities import Transaction, User
from domain.entities.transaction import TransactionStatus
from domain.errors import CouldNotCreateTransaction, CouldNotGetWallets, WalletNotFound
from domain.use_cases import TransferFunds


class TestTransferFunds(TestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

        await load_fixtures(self.database, ['accounts', 'wallets'])

        self.user = User(
            id=constants.FIRST_USER_ID,
            names='Jon',
            last_names='Doe',
            email='jon.doe@example.com',
        )
        self.source_wallet_id = constants.CASH_WALLET_ID
        self.target_wallet_id = constants.BBVA_WALLET_ID
        self.amount = 50.0
        self.concept = 'Groceries'

    async def test_transfer_funds_between_wallets_of_same_user(self):
        transaction = await self.fund_transfers()

        self.assert_that(transaction).is_instance_of(Transaction)
        self.assert_that(transaction.description).is_equal_to(
            'Transfer funds from Cash Wallet to BBVA Wallet'
        )
        self.assert_that(transaction.status).is_equal_to(TransactionStatus.PENDING)
        self.assert_that(transaction.is_balanced()).is_true()
        self.assert_that(transaction.source_entry.account_id).is_equal_to(
            constants.CASH_ACCOUNT_ID
        )
        self.assert_that(transaction.source_entry.amount).is_equal_to(-self.amount)
        self.assert_that(transaction.target_entry.account_id).is_equal_to(
            constants.BBVA_ACCOUNT_ID
        )
        self.assert_that(transaction.target_entry.amount).is_equal_to(self.amount)

    async def test_raises_wallet_not_found_when_source_wallet_does_not_exist(self):
        with self.assertRaises(WalletNotFound):
            await self.fund_transfers(source_wallet_id=uuid4())

    async def test_raises_wallet_not_found_when_source_wallet_does_not_belong_to_user(self):
        other_user = User(
            names='Jane',
            last_names='Doe',
            email='jane.doe@example.com',
            id=constants.SECOND_USER_ID,
        )

        with self.assertRaises(WalletNotFound):
            await self.fund_transfers(user=other_user)

    async def test_raises_wallet_not_found_when_target_wallet_does_not_exist(self):
        with self.assertRaises(WalletNotFound):
            await self.fund_transfers(target_wallet_id=uuid4())

    async def test_raises_could_not_get_wallets_when_database_fails(self):
        with patch.object(self.database.wallets, 'find_by_id') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotGetWallets):
                await self.fund_transfers()

    async def test_raises_could_not_create_transaction_when_database_fails(self):
        with patch.object(self.database.transactions, 'create') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotCreateTransaction):
                await self.fund_transfers()

    async def fund_transfers(self, user: User = None, source_wallet_id: UUID = None, target_wallet_id: UUID = None):
        transfer = TransferFunds(
            self.database,
            user or self.user,
            source_wallet_id or self.source_wallet_id,
            target_wallet_id or self.target_wallet_id,
            self.concept,
            self.amount,
        )

        return await transfer.execute()
