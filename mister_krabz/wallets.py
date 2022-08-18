from database.stores.errors import WalletNotFound as WalletDoesNotExist
from mister_krabz.entities import Wallet
from mister_krabz.errors import (
    CouldntCreateWallet,
    CouldntGetWallets,
    CouldntUpdateWallets,
    WalletNotFound
)


class Wallets:
    def __init__(self, database):
        self._database = database

    async def create(self, name):
        wallet = Wallet(name=name)

        try:
            return await self._database.wallets.create(wallet)
        except Exception as error:
            raise CouldntCreateWallet(error)

    async def update(self, data):
        try:
            wallet = await self._database.wallets.update(data)
        except WalletDoesNotExist as error:
            raise WalletNotFound(id)
        except Exception as error:
            raise CouldntUpdateWallets(error)

        return wallet

    async def get_by_id(self, id):
        try:
            wallet = await self._database.wallets.find_by_id(id)
        except WalletDoesNotExist as error:
            raise WalletNotFound(id)
        except Exception as error:
            raise CouldntGetWallets(error)

        return wallet

    async def get_list(self):
        try:
            wallets = await self._database.wallets.find_all()
        except Exception as error:
            raise CouldntGetWallets(error)

        return wallets
