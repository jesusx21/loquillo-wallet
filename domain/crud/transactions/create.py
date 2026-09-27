from datetime import datetime
from uuid import UUID

from .errors import CouldNotCreateTransaction
from database.stores import Database
from domain.crud.accounts import Accounts
from domain.entities.transaction import TransactionStatus
from domain.entities import Entry, Transaction


class CreateTransaction:
    def __init__(
        self,
        database: Database,
        source_account_id: UUID,
        target_account_id: UUID,
        source_concept: str,
        target_concept: str,
        amount: int,
        date: datetime,
        note: str = None
    ):
        self.__database = database
        self.__source_account_id = source_account_id
        self.__target_account_id = target_account_id
        self.__source_concept = source_concept
        self.__target_concept = target_concept
        self.__amount = amount
        self.__date = date
        self.__note = note

        self.__accounts = Accounts(database)

    async def execute(self):
        transaction = await self.__create_transaction()

        return await self.__save_transaction(transaction)

    async def __create_transaction(self):
        transaction = Transaction(
            status=TransactionStatus.COMPLETED,
            date=self.__date,
            note=self.__note
        )

        source_account = await self.__accounts.get_by_id(self.__source_account_id)
        target_account = await self.__accounts.get_by_id(self.__target_account_id)

        transaction.add_entries(
            Entry(
                account=source_account,
                amount=-self.__amount,
                concept=self.__source_concept
            ),
            Entry(
                account=target_account,
                amount=self.__amount,
                concept=self.__target_concept
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
