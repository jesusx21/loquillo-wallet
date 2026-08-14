from uuid import UUID

from database.stores.errors import NotFound, WalletNotFound
from database.stores.memory.store import MemoryStore
from domain.entities import Wallet


class MemoryWalletsStore(MemoryStore[Wallet]):
    async def update(self, wallet: Wallet):
        try:
            return await super().update(wallet)
        except NotFound as error:
            raise WalletNotFound(wallet.id) from error

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise WalletNotFound(id) from error
