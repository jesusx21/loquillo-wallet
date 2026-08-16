from uuid import UUID

from database.stores.errors import EntryNotFound, NotFound
from database.stores.sql.store import SQLStore
from database.tables import Entries
from domain.entities import Entry


class SQLEntriesStore(SQLStore):
    def __init__(self, database: object):
        super().__init__(database, Entries)

    async def create(self, entry: Entry):
        return await self._create(
            account_id=entry.account_id,
            transaction_id=entry.transaction_id,
            concept=entry.concept,
            amount=entry.amount,
        )

    async def find_by_id(self, entry_id: UUID) -> Entry:
        try:
            return await self._find_by_id(entry_id)
        except NotFound as error:
            raise EntryNotFound(entry_id) from error

    def _build_entity(self, **kwargs) -> Entry:
        return Entry(
            id=kwargs['id'],
            account_id=kwargs.get('account_id'),
            transaction_id=kwargs.get('transaction_id'),
            concept=kwargs['concept'],
            amount=kwargs['amount'],
            created_at=kwargs['created_at'],
            updated_at=kwargs['updated_at']
        )
