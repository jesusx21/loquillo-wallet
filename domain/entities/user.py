from datetime import datetime
from uuid import UUID

from .entity import Entity


class User(Entity):
    def __init__(
        self,
        names: str,
        last_names: str,
        email: str,
        id: UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id, created_at, updated_at)

        self.names = names
        self.last_names = last_names
        self.email = email
