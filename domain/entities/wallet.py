from enum import Enum
from uuid import UUID

from .account import Account
from .entity import Entity
from .errors import EntityAccountsNotSet, EntityAccountsAlreadySet
from domain.core.entity_accounts import EntityAccounts


class WalletType(str, Enum):
    CASH = 'cash'
    DEBIT_CARD = 'debit_card'
    CREDIT_CARD = 'credit_card'


class Wallet(Entity):
    def __init__(
        self,
        name: str,
        type: WalletType,
        user_id: UUID,
        id=None,
        account: Account | None = None,
        account_id: UUID = None,
        created_at=None,
        updated_at=None,
        entity_accounts: EntityAccounts | None = None
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        self.name = name
        self.type = type
        self.user_id = user_id

        self.account_id = account.id if account_id is None and account is not None else account_id

        self.__account = account
        self.__entity_accounts = entity_accounts

    def set_entity_accounts(self, entity_accounts: EntityAccounts):
        if self.__entity_accounts is not None:
            raise EntityAccountsAlreadySet()

        self.__entity_accounts = entity_accounts

    async def get_account(self) -> Account:
        if self.__account is not None:
            return self.__account

        if self.__entity_accounts is None:
            raise EntityAccountsNotSet()

        self.__account = await self.__entity_accounts.find_by_account_id(self.account_id)
        self.account_id = self.__account.id

        return self.__account
