from uuid import UUID

from .store import MemoryStore
from database.stores.errors import NotFound, WalletNotFound
from domain.entities import Wallet


class MemoryWalletsStore(MemoryStore[Wallet]):
    async def update(self, wallet: Wallet):
        try:
            return await super().update(wallet)
        except NotFound:
            raise WalletNotFound(wallet.id)

    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound:
            raise WalletNotFound(id)
