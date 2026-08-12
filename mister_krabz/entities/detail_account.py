form .account import Account


class DetailAccount(Account):
    def __init__(self, name, id=None, parent_id=None, created_at=None, updated_at=None):
        super().__init__(
            id=id,
            name=name,
            type='detail',
            created_at=created_at,
            updated_at=updated_at
        )

        self.parent_id = parent_id
