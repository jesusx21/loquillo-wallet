from uuid import UUID

from domain.errors import DomainError, NotFound


class AccountNotFound(NotFound):
    def __init__(self, account_id: UUID):
        super().__init__(
            message=f'Account with ID {account_id} not found',
            account_id=account_id
        )


class CouldNotCreateAccount(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(message='Could not create an account', cause=cause)


class CouldNotGetAccount(DomainError):
    def __init__(self, account_id: UUID, cause: Exception = None):
        super().__init__(
            f'Could not get account with ID {account_id}',
            cause,
            account_id=account_id
        )
