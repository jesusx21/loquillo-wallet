

from datetime import datetime
from uuid import UUID


class Entity:
    def __init__(
        self,
        id: UUID=None,
        created_at: datetime=None,
        updated_at: datetime=None
    ):
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
