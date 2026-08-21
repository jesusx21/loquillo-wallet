from enum import Enum
from datetime import datetime
from uuid import UUID

from .entity import Entity
from .entry import Entry
from domain.entities.errors import SourceEntryAlreadySet, TargetEntryAlreadySet


class TransactionStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class Transaction(Entity):
    def __init__(
        self,
        description: str,
        status: TransactionStatus,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        super().__init__(id, created_at, updated_at)

        self.description = description
        self.status = status
        self._source_entry: Entry | None = None
        self._target_entry: Entry | None = None

    @property
    def source_entry(self):
        return self._source_entry

    @property
    def target_entry(self):
        return self._target_entry

    @property
    def entries(self):
        entries = []

        if self._source_entry:
            entries.append(self._source_entry)
        if self._target_entry:
            entries.append(self._target_entry)

        return entries

    def is_balanced(self):
        if not self._source_entry or not self._target_entry:
            return False

        return self._source_entry.amount + self._target_entry.amount == 0

    def add_entries(self, *entries: tuple[Entry]):
        [self.add_entry(entry) for entry in entries]

    def add_entry(self, entry: Entry):
        if entry.amount < 0:
            if self._source_entry is not None:
                raise SourceEntryAlreadySet()

            self._source_entry = entry
        else:
            if self._target_entry is not None:
                raise TargetEntryAlreadySet()

            self._target_entry = entry

    def has_source_entry(self):
        return self._source_entry is not None

    def has_target_entry(self):
        return self._target_entry is not None
