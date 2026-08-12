from datetime import datetime
from uuid import UUID

from domain.entities.account import Account
from domain.entities.entity import Entity


class Entry(Entity):
    def __init__(
        self,
        account: Account,
        transaction_id: UUID,
        concept: str,
        amount: float,
        id: UUID = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.account = account
        self.transaction_id = transaction_id
        self.concept = concept
        self.amount = amount
