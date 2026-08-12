from .entity import Entity


class Transaction(Entity):
    def __init__(self, description, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)

        self.description = description
