from uuid import UUID

from .errors import AccountNotFound, CouldNotCreateAccount, CouldNotGetAccount
from database.stores.errors import AccountNotFound as AccountDoesNotExist
from domain.crud.base import CRUDBase
from domain.entities import Account
from domain.entities.account import AccountType


class Accounts(CRUDBase):
    async def create(self, name: str):
        account = Account(name, AccountType.DETAIL)

        try:
            return await self._database.accounts.create(account)
        except Exception as error:
            raise CouldNotCreateAccount(cause=error) from error

    async def get_by_id(self, account_id: UUID):
        try:
            return await self._database.accounts.find_by_id(account_id)
        except AccountDoesNotExist as error:
            raise AccountNotFound(account_id) from error
        except Exception as error:
            raise CouldNotGetAccount(account_id, error) from error
