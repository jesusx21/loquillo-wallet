from datetime import datetime
from uuid import UUID

from domain.entities.entity import Entity


class Entry(Entity):
    def __init__(
        self,
        account_id: UUID,
        concept: str,
        amount: int,
        id: UUID | None = None,
        transaction_id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.account_id = account_id
        self.transaction_id = transaction_id
        self.concept = concept
        self.amount = amount
