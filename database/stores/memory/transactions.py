from uuid import UUID

from database.stores.errors import NotFound, TransactionNotFound
from domain.entities import Transaction
from .store import MemoryStore


class MemoryTransactionsStore(MemoryStore[Transaction]):
    async def update(self, transaction: Transaction):
        try:
            return await super().update(transaction)
        except NotFound:
            raise TransactionNotFound(transaction.id)

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound:
            raise TransactionNotFound(id)
