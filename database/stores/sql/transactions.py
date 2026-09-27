from uuid import UUID

from database.stores.errors import NotFound, TransactionNotFound
from database.stores.sql.store import SQLStore
from database.tables import Transactions
from domain.entities import Transaction
from domain.entities.transaction import TransactionStatus


class SQLTransactionsStore(SQLStore):
    def __init__(self, database: object):
        super().__init__(database, Transactions)

    async def create(self, transaction: Transaction):
        return await self._create(
            status=transaction.status.value,
            date=transaction.date,
            note=transaction.note
        )

    async def find_by_id(self, transaction_id: UUID) -> Transaction:
        try:
            return await self._find_by_id(transaction_id)
        except NotFound as error:
            raise TransactionNotFound(transaction_id) from error

    def _build_entity(self, **kwargs) -> Transaction:
        return Transaction(
            id=kwargs['id'],
            status=TransactionStatus(kwargs['status']),
            note=kwargs['note'],
            date=kwargs['date'],
            created_at=kwargs['created_at']
        )
