from enum import Enum
from uuid import UUID

from .entity import Entity
from .errors import WalletEntriesNotSet, WalletEntriesAlreadySet
from domain.core.wallet_entries import WalletEntries


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
        account_id: UUID = None,
        created_at=None,
        updated_at=None,
        wallet_entries: WalletEntries | None = None
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        self.name = name
        self.type = type
        self.account_id = account_id
        self.user_id = user_id

        self.__wallet_entries = wallet_entries

    def set_wallet_entries(self, wallet_entries: WalletEntries):
        if self.__wallet_entries is not None:
            raise WalletEntriesAlreadySet()

        self.__wallet_entries = wallet_entries

    def has_wallet_entries(self) -> bool:
        return self.__wallet_entries is not None

    async def get_balance(self) -> int:
        if self.__wallet_entries is None:
            raise WalletEntriesNotSet()

        return await self.__wallet_entries.get_balance()
