from domain.errors import DomainError


class EntityError(DomainError):
    def __init__(self, message: str, cause: Exception | None = None, **kwargs):
        super().__init__(message=message, cause=cause, **kwargs)


class SourceEntryAlreadySet(EntityError):
    def __init__(self):
        super().__init__(
            message='Source entry is already set'
        )


class TargetEntryAlreadySet(EntityError):
    def __init__(self):
        super().__init__(
            message='Target entry is already set'
        )
