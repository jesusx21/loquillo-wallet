from .entry import Entry
from .entity import Entity


class Transaction(Entity):
    def __init__(
        self,
        description: str,
        id=None,
        entries: list[Entry] = [],
        created_at=None,
        updated_at=None
    ):
        super().__init__(id, created_at, updated_at)

        self.description = description
        self.entries = entries
