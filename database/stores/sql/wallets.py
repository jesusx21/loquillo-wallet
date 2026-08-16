from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncEngine

from .store import SQLStore
from database.stores.errors import NotFound, WalletNotFound
from database.tables.wallets import Wallets
from domain.entities import Wallet
from domain.entities.wallet import WalletType


class SQLWalletsStore(SQLStore):
    def __init__(self, engine: AsyncEngine):
        super().__init__(engine, Wallets)

    async def create(self, wallet: Wallet):
        return await self._create(
            name=wallet.name,
            type=wallet.type.value,
            account_id=wallet.account_id
        )

    async def find_by_id(self, wallet_id: UUID) -> Wallet:
        try:
            return await self._find_by_id(wallet_id)
        except NotFound as error:
            raise WalletNotFound(wallet_id) from error

    def _build_entity(self, **kwargs) -> Wallet:
        return Wallet(
            id=kwargs['id'],
            name=kwargs['name'],
            type=WalletType(kwargs['type']),
            account_id=kwargs['account_id'],
            created_at=kwargs['created_at']
        )
