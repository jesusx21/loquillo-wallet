from datetime import datetime
from enum import Enum
from uuid import UUID

from .entity import Entity


class AccountType(str, Enum):
    DETAIL = "detail"
    SUMMARY = "summary"


class Account(Entity):
    def __init__(
        self,
        name: str,
        type: AccountType,
        id: UUID=None,
        created_at: datetime=None,
        updated_at: datetime=None
    ):
        super().__init__(id, created_at, updated_at)

        self.name = name
        self.type = type
