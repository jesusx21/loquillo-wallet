from uuid import UUID

from database.stores.errors import NotFound, TransactionNotFound
from database.stores.memory.store import MemoryStore
from domain.entities import Transaction


class MemoryTransactionsStore(MemoryStore[Transaction]):
    async def update(self, transaction: Transaction):
        try:
            return await super().update(transaction)
        except NotFound as error:
            raise TransactionNotFound(transaction.id) from error

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise TransactionNotFound(id) from error
