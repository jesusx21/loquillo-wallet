from domain.errors import DomainError


class EntityError(DomainError):
    def __init__(self, message: str, cause: Exception | None = None, **kwargs):
        super().__init__(message=message, cause=cause, **kwargs)


class SourceEntryAlreadySet(EntityError):
    def __init__(self):
        super().__init__(
            message='Source entry is already set'
        )


class SourceAccountAlreadySet(EntityError):
    def __init__(self):
        super().__init__(
            message='Source account is already set'
        )


class TargetEntryAlreadySet(EntityError):
    def __init__(self):
        super().__init__(
            message='Target entry is already set'
        )


class PostingRuleNotDefineForEvent(NotImplementedError):
    def __init__(self, event_type: str):
        super().__init__(
            message=f'Posting rule not defined for event type: {event_type}'
        )


class EntityAccountsAlreadySet(EntityError):
    def __init__(self):
        super().__init__(
            message='Entity accounts are already set'
        )


class EntityAccountsNotSet(EntityError):
    def __init__(self):
        super().__init__(
            message='Entity accounts are not set'
        )


class CannotHaveDifferentAccountTypes(EntityError):
    def __init__(self):
        super().__init__(
            message='Cannot have different account types in the same transaction'
        )


class NoSourceAccount(EntityError):
    def __init__(self):
        super().__init__(
            message='No source account is set for the transaction'
        )
