from datetime import datetime
from uuid import UUID


class Entity:
    def __init__(
        self,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None
    ):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
