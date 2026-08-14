from datetime import datetime
from uuid import UUID

from .entity import Entity
from .entry import Entry


class Transaction(Entity):
    def __init__(
        self,
        description: str,
        id: UUID = None,
        entries: list[Entry] = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.description = description
        self.entries = entries or []
