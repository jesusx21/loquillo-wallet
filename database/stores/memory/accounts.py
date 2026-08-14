from uuid import UUID

from database.stores.errors import AccountNotFound, NotFound
from database.stores.memory.store import MemoryStore
from domain.entities import Account


class MemoryAccountsStore(MemoryStore[Account]):
    async def update(self, account: Account):
        try:
            return await super().update(account)
        except NotFound as error:
            raise AccountNotFound(account.id) from error

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise AccountNotFound(id) from error
