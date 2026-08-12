from entities.account import Account


class Entry:
    def __init__(self, account: Account, concept: str, amount: float):
        self.account = account
        self.concept = concept
        self.amount = amount
