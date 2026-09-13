from uuid import UUID

from database import Database
from database.stores.errors import WalletNotFound as WalletDoesNotExist
from domain.entities import Entry, Transaction, User, Wallet
from domain.entities.transaction import TransactionStatus
from domain.errors import CouldNotCreateTransaction, WalletNotFound, CouldNotGetWallets


class TransferFunds:
    def __init__(
        self,
        database: Database,
        user: User,
        source_wallet_id: UUID,
        target_wallet_id: UUID,
        amount: float
    ):
        self.__database = database
        self.__user = user
        self.__source_wallet_id = source_wallet_id
        self.__target_wallet_id = target_wallet_id
        self.__amount = amount

    async def execute(self):
        source_wallet = await self._get_wallet(self.__source_wallet_id)
        target_wallet = await self._get_wallet(self.__target_wallet_id)

        transaction = await self.__create_transaction(source_wallet, target_wallet)

        return await self.__save_transaction(transaction)

    async def _get_wallet(self, wallet_id: UUID):
        try:
            wallet = await self.__database.wallets.find_by_id(wallet_id)
        except WalletDoesNotExist as error:
            raise WalletNotFound(wallet_id=wallet_id) from error
        except Exception as error:
            raise CouldNotGetWallets(cause=error) from error

        if wallet.user_id != self.__user.id:
            raise WalletNotFound(wallet_id=wallet_id)

        return wallet

    async def __create_transaction(self, source_wallet: Wallet, target_wallet: Wallet):
        transaction = Transaction(
            description=f'Transfer funds from {source_wallet.name} to {target_wallet.name}',
            status=TransactionStatus.COMPLETED,
        )

        transaction.add_entries(
            Entry(
                account=await source_wallet.get_account(),
                amount=-self.__amount,
                concept=f'Transfer to {target_wallet.name}.'
            ),
            Entry(
                account=await target_wallet.get_account(),
                amount=self.__amount,
                concept=f'Transfer from {source_wallet.name}.'
            )
        )

        return transaction

    async def __save_transaction(self, transaction_to_save: Transaction):
        async with self.__database.transacting() as database:
            try:
                transaction = await database.transactions.create(transaction_to_save)

                for entry in transaction_to_save.entries:
                    entry.transaction_id = transaction.id

                    await database.entries.create(entry)
            except Exception as error:
                raise CouldNotCreateTransaction(cause=error) from error

        return transaction
