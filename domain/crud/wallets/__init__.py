from uuid import UUID

from .errors import CouldNotCreateWallet, CouldNotGetWallets, WalletNotFound, CouldNotGetWallet
from database.stores.errors import WalletNotFound as WalletDoesNotExist
from domain.crud.accounts import Accounts
from domain.crud.base import CRUDBase
from domain.entities.wallet import Wallet, WalletType


class Wallets(CRUDBase):
    async def create(self, user_id: UUID, name: str, type: WalletType):
        accounts = Accounts(self._database)

        account = await accounts.create(f'Cuenta de {name}')
        wallet = Wallet(name, type, user_id, account_id=account.id)

        try:
            return await self._database.wallets.create(wallet)
        except Exception as error:
            raise CouldNotCreateWallet(cause=error) from error

    async def get_by_id(self, wallet_id: UUID):
        try:
            return await self._database.wallets.find_by_id(wallet_id)
        except WalletDoesNotExist as error:
            raise WalletNotFound(wallet_id) from error
        except Exception as error:
            raise CouldNotGetWallet(wallet_id, error) from error

    async def get_by_types(self, user_id: UUID, types: list[WalletType]):
        try:
            return await self._database.wallets.find(
                user_id=user_id,
                type=[wallet_type.value for wallet_type in types]
            )
        except Exception as error:
            raise CouldNotGetWallets(cause=error) from error
