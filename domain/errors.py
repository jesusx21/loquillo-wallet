class DomainError(Exception):
    def __init__(self, message: str = None, cause: Exception = None, **kwargs):
        super().__init__(message)
        self.cause = cause
        self.info = kwargs


class CouldNotCreateAccount(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(message='Could not create an account', cause=cause)


class CouldNotCreateWallet(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(message='Could not create a wallet', cause=cause)


class CouldNotCreateUser(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(message='Could not create a user', cause=cause)


class CouldNotGetWallets(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(message='Could not get wallets', cause=cause)


class NotFound(DomainError):
    def __init__(self, message: str, cause=None, **kwargs):
        super().__init__(message=message, cause=cause, **kwargs)


class AccountNotFound(DomainError):
    def __init__(self, account_id: str, cause: Exception = None):
        super().__init__(
            message=f'Account with ID {account_id} not found', account_id=account_id, cause=cause
        )


class WalletNotFound(DomainError):
    def __init__(self, wallet_id: str, cause: Exception = None):
        super().__init__(
            message=f'Wallet with ID {wallet_id} not found', wallet_id=wallet_id, cause=cause
        )


class CouldNotCreateTransaction(DomainError):
    def __init__(self, cause: Exception = None):
        super().__init__(
            message='Could not create transaction', cause=cause
        )


class CouldNotGetAccount(DomainError):
    def __init__(self, cause: Exception = None):
        super().__init__(
            message='Could not get accounts', cause=cause
        )


class CouldNotCreateCategories(DomainError):
    def __init__(self, cause: Exception = None, **kwargs):
        super().__init__(
            message='Could not create categories', cause=cause, **kwargs
        )
