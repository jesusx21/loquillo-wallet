from uuid import UUID


class DatabaseError(Exception): pass # noqa
class NotFound(DatabaseError): pass # noqa


class InvalidId(DatabaseError):
    def __init__(self, id: UUID):
        self.id = id


class AccountNotFound(NotFound):
    def __init__(self, id: UUID):
        self.id = id


class EntryNotFound(NotFound):
    def __init__(self, id: UUID):
        self.id = id


class TransactionNotFound(NotFound):
    def __init__(self, id: UUID):
        self.id = id
