from database.stores.memory.accounts import AccountsStore
from database.stores.memory.wallets import WalletsStore


class InMemoryDatabase:
    def __init__(self):
        self.accounts = AccountsStore()
        self.wallets = WalletsStore()
