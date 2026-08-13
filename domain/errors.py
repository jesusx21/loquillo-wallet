class DomainError(Exception):
    def __init__(
        self,
        message: str = None,
        cause: Exception = None,
        **kwargs
    ):
        super().__init__(message)
        self.cause = cause
        self.info = kwargs


class CouldNotCreateAccount(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(
            message='Could not create an account',
            cause=cause
        )


class CouldNotCreateWallet(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(
            message='Could not create a wallet',
            cause=cause
        )
