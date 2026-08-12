from .account import Account


class SummaryAccount(Account):
    def __init__(self, name, id=None, created_at=None, updated_at=None):
        super().__init__(
            id=id,
            name=name,
            type='summary',
            created_at=created_at,
            updated_at=updated_at
        )

        self.children = []
