from uuid import UUID

from domain.errors import DomainError


class ReadOnlyField(DomainError):
    def __init__(self, field: str):
        super().__init__(
            message=f'Field {field} is read-only',
            field=field
        )


class CouldNotLoadAccount(DomainError):
    def __init__(self, account_id: UUID, cause: Exception):
        super().__init__(
            message=f'Could not load account with id {account_id}',
            account_id=account_id,
            cause=cause
        )
