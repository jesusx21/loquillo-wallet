from database.stores.memory.wallets import WalletsStore


class InMemoryDatabase:
    def __init__(self):
        self.wallets = WalletsStore()
