from uuid import UUID

from .store import MemoryStore
from database.stores.errors import AccountNotFound, NotFound
from domain.entities import Account


class MemoryAccountsStore(MemoryStore[Account]):
    async def update(self, account: Account):
        try:
            return await super().update(account)
        except NotFound:
            raise AccountNotFound(account.id)

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound:
            raise AccountNotFound(id)
