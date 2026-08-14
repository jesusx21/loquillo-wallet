from datetime import datetime
from uuid import UUID

from domain.entities.errors import SourceEntryAlreadySet

from .entity import Entity
from .entry import Entry


class Transaction(Entity):
    def __init__(
        self,
        description: str,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        super().__init__(id, created_at, updated_at)

        self.description = description
        self._source_entry: Entry | None = None
        self._target_entries: list[Entry] | None = []

    @property
    def source_entry(self):
        return self._source_entry

    @property
    def target_entries(self):
        return self._target_entries

    @property
    def entries(self):
        if self._source_entry:
            return [self._source_entry] + self._target_entries

        return self._target_entries

    def is_balanced(self):
        if not self._source_entry or not self._target_entries:
            return False

        total_target_amount = sum(entry.amount for entry in self._target_entries)

        return self._source_entry.amount + total_target_amount == 0

    def add_entries(self, *entries: tuple[Entry]):
        [self.add_entry(entry) for entry in entries]

    def add_entry(self, entry: Entry):
        if entry.amount < 0:
            if self._source_entry is not None:
                raise SourceEntryAlreadySet()

            self._source_entry = entry
        else:
            self._target_entries.append(entry)

    def has_source_entry(self):
        return self._source_entry is not None

    def has_target_entry(self):
        return len(self._target_entries) > 0
