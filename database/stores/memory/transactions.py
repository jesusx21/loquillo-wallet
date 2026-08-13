from uuid import UUID

from .store import MemoryStore
from database.stores.errors import NotFound, TransactionNotFound
from domain.entities import Transaction


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
