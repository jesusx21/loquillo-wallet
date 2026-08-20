from uuid import UUID

from .store import SQLStore
from database.stores.errors import NotFound, WalletNotFound
from database.tables.wallets import Wallets
from domain.entities import Wallet
from domain.entities.wallet import WalletType


class SQLWalletsStore(SQLStore):
    def __init__(self, database: object):
        super().__init__(database, Wallets)

    async def create(self, wallet: Wallet):
        return await self._create(
            name=wallet.name,
            type=wallet.type.value,
            account_id=wallet.account_id,
            user_id=wallet.user_id
        )

    async def find_by_id(self, wallet_id: UUID) -> Wallet:
        try:
            return await self._find_by_id(wallet_id)
        except NotFound as error:
            raise WalletNotFound(wallet_id) from error

    async def find_by_user_id(self, user_id: UUID) -> Wallet:
        try:
            return await self._find_one(user_id=user_id)
        except NotFound as error:
            raise WalletNotFound(user_id) from error

    async def find(self, **filters) -> list[Wallet]:
        return await self._find(**filters)

    def _build_entity(self, **kwargs) -> Wallet:
        return Wallet(
            id=kwargs['id'],
            name=kwargs['name'],
            type=WalletType(kwargs['type']),
            account_id=kwargs['account_id'],
            user_id=kwargs['user_id'],
            created_at=kwargs['created_at'],
            updated_at=kwargs['updated_at']
        )
