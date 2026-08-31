from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from domain.core.errors import CouldNotLoadEventAccounts, CouldNotLoadEventEntities, ReadOnlyField

if TYPE_CHECKING:
    from database.stores import Database


class Event:
    def __init__(
        self,
        id: UUID = None,
        date: datetime = None,
        created_at: datetime = None,
        **kwargs
    ):
        self._id = id
        self._date = date
        self._created_at = created_at

        self._resulting_transactions = []
        self._triggered_events = []

        self.__are_entities_loaded = False
        self.__are_accounts_loaded = False

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @id.setter
    def id(self, value: UUID):
        if self._id is not None:
            raise ReadOnlyField('id')

        self._id = value

    @date.setter
    def date(self, value: datetime):
        if self._date is not None:
            raise ReadOnlyField('date')

        self._date = value

    @created_at.setter
    def created_at(self, value: datetime):
        if self._created_at is not None:
            raise ReadOnlyField('created_at')

        self._created_at = value

    def add_resulting_transaction(self, transaction):
        self._resulting_transactions.append(transaction)

    def add_triggered_event(self, event):
        self._triggered_events.append(event)

    async def process(self):
        raise NotImplementedError()

    def get_metadata(self) -> dict:
        raise NotImplementedError()

    async def load_entities(self, database: Database):
        if self.__are_entities_loaded:
            return

        try:
            await self._load_entities(database)

            self._mark_entities_as_loaded()
        except Exception as error:
            raise CouldNotLoadEventEntities(self.type, cause=error) from error

    async def load_accounts(self, database: Database):
        if self.__are_accounts_loaded:
            return

        if not self.__are_entities_loaded:
            raise CouldNotLoadEventAccounts('Call load_entities before load_accounts')

        try:
            await self._load_accounts(database)

            self._mark_accounts_as_loaded()
        except Exception as error:
            raise CouldNotLoadEventAccounts(cause=error) from error

    async def _load_entities(self, database: Database) -> None:
        raise NotImplementedError('load_entities is not implemented.')

    async def _load_accounts(self, database: Database) -> None:
        raise NotImplementedError('load_accounts is not implemented.')

    def _mark_entities_as_loaded(self):
        self.__are_entities_loaded = True

    def _mark_accounts_as_loaded(self):
        self.__are_accounts_loaded = True
