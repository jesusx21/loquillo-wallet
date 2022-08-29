from mister_krabz.entities.entity import Entity


class Wallet(Entity):
    def __init__(self, name, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)

        self.name = name
