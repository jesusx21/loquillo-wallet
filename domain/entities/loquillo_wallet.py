from datetime import datetime
from uuid import UUID

from domain.entities.entity import Entity


class LoquilloWallet(Entity):
    def __init__(
        self,
        user_id: UUID,
        incomes_account_id: UUID,
        expenses_account_id: UUID,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.user_id = user_id
        self.incomes_account_id = incomes_account_id
        self.expenses_account_id = expenses_account_id
