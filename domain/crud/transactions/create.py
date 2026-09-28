from datetime import datetime
from uuid import UUID

from .errors import CouldNotCreateTransaction
from database.stores import Database
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

    async def execute(self):
        async with self.__database.transacting() as database:
            self.__database = database

            try:
                transaction = await self.__save_transaction()
                transaction.add_entries(
                    await self.__save_source_entry(transaction.id),
                    await self.__save_target_entry(transaction.id)
                )
            except Exception as error:
                raise CouldNotCreateTransaction(cause=error) from error

        return transaction

    async def __save_transaction(self):
        transaction = Transaction(
            status=TransactionStatus.COMPLETED,
            date=self.__date,
            note=self.__note
        )

        return await self.__database.transactions.create(transaction)

    async def __save_source_entry(self, transaction_id: UUID):
        entry = Entry(
            transaction_id=transaction_id,
            account_id=self.__source_account_id,
            amount=self.__amount * -1,
            concept=self.__source_concept
        )

        return await self.__database.entries.create(entry)

    async def __save_target_entry(self, transaction_id: UUID):
        entry = Entry(
            transaction_id=transaction_id,
            account_id=self.__target_account_id,
            amount=self.__amount,
            concept=self.__target_concept
        )

        return await self.__database.entries.create(entry)
