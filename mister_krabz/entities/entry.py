from .entity import Entity


class Entry(Entity):
    def __init__(self, transaction_id, account_id, concept, amount, id=None, created_at=None):
        super().__init__(id=id, created_at=created_at)

        self.transaction_id = transaction_id
        self.account_id = account_id
        self.concept = concept
        self.amount = amount
