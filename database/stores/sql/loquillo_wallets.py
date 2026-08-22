from uuid import UUID

from database.stores.errors import DatabaseError
from database.stores.sql.store import SQLStore
from database.tables import LoquilloWallets
from domain.entities import LoquilloWallet


class SQLLoquilloWalletsStore(SQLStore):
    def __init__(self, database: object):
        super().__init__(database, LoquilloWallets)

    async def create(self, loquillo_wallet: LoquilloWallet):
        return await self._create(
            user_id=loquillo_wallet.user_id,
            incomes_account_id=loquillo_wallet.incomes_account_id,
            expenses_account_id=loquillo_wallet.expenses_account_id,
        )

    async def find_by_user_id(self, user_id: UUID) -> LoquilloWallet:
        try:
            return await self._find_one(user_id=user_id)
        except Exception as error:
            raise DatabaseError(user_id) from error

    def _build_entity(self, **kwargs) -> LoquilloWallet:
        return LoquilloWallet(
            id=kwargs['id'],
            user_id=kwargs['user_id'],
            incomes_account_id=kwargs['incomes_account_id'],
            expenses_account_id=kwargs['expenses_account_id']
        )
