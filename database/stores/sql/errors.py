from database.stores.errors import DatabaseError


class TransactionNotOpened(DatabaseError):
    def __init__(self):
        super().__init__(message='Transaction not opened.')
