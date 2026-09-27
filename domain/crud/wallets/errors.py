from uuid import UUID

from domain.errors import DomainError, NotFound


class CouldNotCreateWallet(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(message='Could not create a wallet', cause=cause)


class CouldNotGetWallet(DomainError):
    def __init__(self, wallet_id: UUID, cause: Exception):
        super().__init__(
            f'Could not get wallet with ID {wallet_id}',
            cause=cause,
            wallet_id=wallet_id
        )


class CouldNotGetWallets(DomainError):
    def __init__(self, cause: Exception):
        super().__init__(message='Could not get wallets', cause=cause)


class WalletNotFound(NotFound):
    def __init__(self, wallet_id: str):
        super().__init__(
            message=f'Wallet with ID {wallet_id} not found',
            wallet_id=wallet_id
        )
