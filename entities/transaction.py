from .entry import Entry

class Transaction:
    def __init__(self, description, entries: list[Entry], id=None):
        self.id = id
        self.description = description
        self.entries = entries
