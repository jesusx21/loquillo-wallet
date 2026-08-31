from datetime import datetime
from uuid import UUID

from domain.entities.account import Account
from domain.entities.entity import Entity
from domain.entities.errors import EntityAccountsNotSet, EntityAccountsAlreadySet
from domain.core.entity_accounts import EntityAccounts


class Entry(Entity):
    def __init__(
        self,
        concept: str,
        amount: int,
        id: UUID | None = None,
        account_id: UUID | None = None,
        account: Account | None = None,
        transaction_id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        entity_accounts: EntityAccounts | None = None
    ):
        super().__init__(id, created_at, updated_at)

        self.transaction_id = transaction_id
        self.concept = concept
        self.amount = amount

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

        return self.__account
