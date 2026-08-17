from enum import Enum
from uuid import UUID

from .entity import Entity


class WalletType(str, Enum):
    CASH = 'cash'
    DEBIT_CARD = 'debit_card'
    CREDIT_CARD = 'credit_card'


class Wallet(Entity):
    def __init__(
        self,
        name: str,
        type: WalletType,
        account_id: UUID,
        user_id: UUID,
        id=None,
        created_at=None,
        updated_at=None
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        self.name = name
        self.type = type
        self.account_id = account_id
        self.user_id = user_id
