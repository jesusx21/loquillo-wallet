from .entity import Entity


class Account(Entity):
    def __init__(self, name, type, id=None, created_at=None, updated_at=None):
        super().__init__(id=id, , created_at=created_at, updated_at=updated_at)

        self.name = name
        self.type = type
