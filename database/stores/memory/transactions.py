from database.stores.memory.store import MemoryStore


class TransactionsStore:
    def __init__(self):
        self._store = MemoryStore()
