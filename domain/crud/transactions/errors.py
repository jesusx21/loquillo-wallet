from domain.errors import DomainError


class CouldNotCreateTransaction(DomainError):
    def __init__(self, cause: Exception = None):
        super().__init__(
            message='Could not create transaction', cause=cause
        )
