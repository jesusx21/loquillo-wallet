from datetime import datetime
from uuid import UUID

from .account import Account, AccountType


class DetailAccount(Account):
    def __init__(
        self, name: str, id: UUID = None, created_at: datetime = None, updated_at: datetime = None
    ):
        super().__init__(
            id=id, name=name, type=AccountType.DETAIL, created_at=created_at, updated_at=updated_at
        )
