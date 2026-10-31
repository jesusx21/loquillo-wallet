from uuid import UUID

from database.stores.errors import NotFound, WalletNotFound
from database.stores.memory.store import MemoryStore
from domain.core.wallet_entries import WalletEntries
from domain.entities import Wallet


class MemoryWalletsStore(MemoryStore[Wallet]):
    def __init__(self, database: object):
        super().__init__()

        self.__database = database

    async def create(self, wallet: Wallet):
        if not wallet.has_wallet_entries():
            wallet.set_wallet_entries(WalletEntries(self.__database, wallet.account_id))

        return await super().create(wallet)

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

    async def find_by_user_id(self, user_id: UUID) -> Wallet:
        return await self._find(user_id=user_id)

    async def find(self, **filters) -> list[Wallet]:
        return await self._find(**filters)
