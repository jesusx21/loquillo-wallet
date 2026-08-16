from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncEngine

from database.stores.errors import NotFound, TransactionNotFound
from database.stores.sql.store import SQLStore
from database.tables import Transactions
from domain.entities import Transaction
from domain.entities.transaction import TransactionStatus


class SQLTransactionsStore(SQLStore):
    def __init__(self, engine: AsyncEngine):
        super().__init__(engine, Transactions)

    async def create(self, transaction: Transaction):
        # TODO: Add database transaction to create entries along with the transaction
        # to ensure atomicity of the operation
        return await self._create(
            description=transaction.description,
            status=transaction.status.value
        )

    async def find_by_id(self, transaction_id: UUID) -> Transaction:
        try:
            return await self._find_by_id(transaction_id)
        except NotFound as error:
            raise TransactionNotFound(transaction_id) from error

    def _build_entity(self, **kwargs) -> Transaction:
        return Transaction(
            id=kwargs['id'],
            description=kwargs['description'],
            status=TransactionStatus(kwargs['status']),
            created_at=kwargs['created_at']
        )
