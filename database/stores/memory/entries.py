from database.stores.memory.store import MemoryStore


class EntriesStore:
    def __init__(self):
        self._store = MemoryStore()
