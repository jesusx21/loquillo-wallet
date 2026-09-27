class DomainError(Exception):
    def __init__(self, message: str = None, cause: Exception = None, **kwargs):
        super().__init__(message)
        self.cause = cause
        self.info = kwargs


class CouldNotCreateUser(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(message='Could not create a user', cause=cause)


class NotFound(DomainError):
    def __init__(self, message: str, cause=None, **kwargs):
        super().__init__(message=message, cause=cause, **kwargs)


class InvalidOperation(DomainError):
    def __init__(self, message: str = 'Invalid operation', **kwargs):
        super().__init__(message=message,  **kwargs)
