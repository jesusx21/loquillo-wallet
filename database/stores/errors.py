class DatabaseError(Exception): pass # noqa
class NotFound(DatabaseError): pass # noqa


class InvalidId(DatabaseError):
    def __init__(self, id):
        self.id = id


class WalletNotFound(NotFound):
    def __init__(self, id):
        self.id = id
