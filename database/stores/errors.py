from uuid import UUID


class DatabaseError(Exception):
    def __init__(self, message: str | None = None, cause: Exception | None = None, **kwargs):
        super().__init__(message=message or 'Unexpected database error', cause=cause, **kwargs)


class NotFound(DatabaseError):
    def __init__(self, message: str | None = None, **kwargs):
        super().__init__(message=message or 'Resource not found', **kwargs)


class InvalidId(DatabaseError):
    def __init__(self, id: UUID):
        super().__init__(message=f'Invalid ID: {id}', id=id)


class AccountNotFound(NotFound):
    def __init__(self, id: UUID):
        super().__init__(message=f'Account not found: {id}', id=id)


class EntryNotFound(NotFound):
    def __init__(self, id: UUID):
        super().__init__(message=f'Entry not found: {id}', id=id)


class TransactionNotFound(NotFound):
    def __init__(self, id: UUID):
        super().__init__(message=f'Transaction not found: {id}', id=id)


class WalletNotFound(NotFound):
    def __init__(self, id: UUID):
        super().__init__(message=f'Wallet not found: {id}', id=id)


class TransactionNotBalanced(DatabaseError):
    def __init__(self):
        super().__init__(message='Transaction not balanced')
