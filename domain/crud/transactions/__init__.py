from datetime import datetime
from uuid import UUID

from domain.crud.base import CRUDBase
from .create import CreateTransaction


class Transactions(CRUDBase):
    async def create(
        self,
        source_account_id: UUID,
        target_account_id: UUID,
        source_concept: str,
        target_concept: str,
        amount: int,
        date: datetime | None = None,
        note: str | None = None,
    ):
        create_transaction = CreateTransaction(
            database=self._database,
            source_account_id=source_account_id,
            target_account_id=target_account_id,
            source_concept=source_concept,
            target_concept=target_concept,
            amount=amount,
            date=date,
            note=note
        )

        return await create_transaction.execute()
