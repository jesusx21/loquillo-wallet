from uuid import UUID

from domain.errors import DomainError


class ReadOnlyField(DomainError):
    def __init__(self, field: str):
        super().__init__(
            message=f'Field {field} is read-only',
            field=field
        )


class CouldNotLoadEventEntities(DomainError):
    def __init__(self, event_type: str, cause: Exception):
        super().__init__(
            message=f'Could not load entities for event type {event_type}',
            event_type=event_type,
            cause=cause
        )


class CouldNotLoadEventAccounts(DomainError):
    def __init__(self, message: str = None, **kwargs):
        super().__init__(
            message=message or 'Could not load accounts for event',
            **kwargs
        )


class CouldNotLoadAccount(DomainError):
    def __init__(self, account_id: UUID, cause: Exception):
        super().__init__(
            message=f'Could not load account with id {account_id}',
            account_id=account_id,
            cause=cause
        )
