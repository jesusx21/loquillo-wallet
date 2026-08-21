from uuid import UUID

from database.stores.errors import NotFound, TransactionNotFound
from database.stores.memory.store import MemoryStore
from domain.entities import Transaction


class MemoryTransactionsStore(MemoryStore[Transaction]):
    def __init__(self, database: object):
        super().__init__()

        self._database = database

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise TransactionNotFound(id) from error
