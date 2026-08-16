from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncEngine

from database.stores.errors import AccountNotFound, NotFound
from database.stores.sql.store import SQLStore
from database.tables import Accounts
from domain.entities import Account, DetailAccount
from domain.entities.account import AccountType


class SQLAccountsStore(SQLStore):
    def __init__(self, engine: AsyncEngine):
        super().__init__(engine, Accounts)

    async def create(self, account: Account):
        return await self._create(
            name=account.name,
            type=account.type.value
        )

    async def find_by_id(self, id: UUID) -> Account:
        try:
            return await self._find_by_id(id)
        except NotFound as error:
            raise AccountNotFound(id) from error

    def _build_entity(self, **kwargs) -> Account:
        if kwargs['type'] == 'detail':
            return DetailAccount(
                id=kwargs['id'],
                name=kwargs['name'],
                created_at=kwargs['created_at'],
                updated_at=kwargs['updated_at']
            )

        return Account(
            id=kwargs['id'],
            name=kwargs['name'],
            type=AccountType(kwargs['type']),
            created_at=kwargs['created_at'],
            updated_at=kwargs['updated_at']
        )
