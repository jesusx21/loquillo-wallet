from uuid import UUID

from database.stores.errors import NotFound, TransactionNotBalanced, TransactionNotFound
from database.stores.memory.store import MemoryStore
from domain.entities import Transaction


class MemoryTransactionsStore(MemoryStore[Transaction]):
    def __init__(self, database: object):
        super().__init__()

        self._database = database

    async def create(self, transaction: Transaction):
        if not transaction.is_balanced():
            raise TransactionNotBalanced()

        # TODO: Run into a database transaction to ensure atomicity of the operation
        transaction_saved = await super().create(transaction)
        transaction_saved._source_entry = None
        transaction_saved._target_entries = []

        for entry in transaction.entries:
            entry.transaction_id = transaction_saved.id

            transaction_saved.add_entry(
                await self._database.entries.create(entry)
            )

        return await self._database.transactions.find_by_id(transaction_saved.id)

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise TransactionNotFound(id) from error
