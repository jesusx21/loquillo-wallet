from uuid import UUID

from .base_use_case import BaseUseCase
from database import Database
from database.stores.errors import WalletNotFound as WalletDoesNotExist
from domain.entities import Entry, Transaction, User
from domain.entities.transaction import TransactionStatus
from domain.errors import CouldNotCreateTransaction, WalletNotFound, CouldNotGetWallets


class TransferFunds(BaseUseCase):
    def __init__(
        self,
        database: Database,
        user: User,
        source_wallet_id: UUID,
        target_wallet_id: UUID,
        concept: str,
        amount: float
    ):
        self._database = database
        self._user = user
        self._source_wallet_id = source_wallet_id
        self._target_wallet_id = target_wallet_id
        self._concept = concept
        self._amount = amount

    async def execute(self):
        async with self._execute_within_transaction():
            source_wallet = await self._get_wallet(self._source_wallet_id)

            if source_wallet.user_id != self._user.id:
                raise WalletNotFound(wallet_id=self._source_wallet_id)

            target_wallet = await self._get_wallet(self._target_wallet_id)
            transaction = self._build_transaction(source_wallet, target_wallet)

            transaction = await self._save_transaction(transaction)

            return transaction

    async def _get_wallet(self, wallet_id: UUID):
        try:
            return await self._database.wallets.find_by_id(wallet_id)
        except WalletDoesNotExist as error:
            raise WalletNotFound(wallet_id=wallet_id) from error
        except Exception as error:
            raise CouldNotGetWallets(cause=error) from error

    def _build_transaction(self, source_wallet, target_wallet):
        transaction = Transaction(
            description=f'Transfer funds from {source_wallet.name} to {target_wallet.name}',
            status=TransactionStatus.PENDING,
        )

        transaction.add_entries(
            Entry(
                account_id=source_wallet.account_id,
                amount=-self._amount,
                concept=self._concept
            ),
            Entry(
                account_id=target_wallet.account_id,
                amount=self._amount,
                concept=self._concept
            )
        )

        return transaction

    async def _save_transaction(self, transaction: Transaction):
        try:
            transaction_saved = await self._database.transactions.create(transaction)
            source_entry = await self._database.entries.create(transaction.source_entry)
            target_entry = await self._database.entries.create(transaction.target_entry)
        except Exception as error:
            raise CouldNotCreateTransaction(cause=error) from error

        transaction_saved._source_entry = source_entry
        transaction_saved._target_entry = target_entry

        return transaction_saved
