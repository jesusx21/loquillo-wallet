from tkinter import N
from database.stores.errors import WalletNotFound as WalletDoesNotExist
from mister_krabz.entities import Wallet
from mister_krabz.entities.account import Account
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
        account = Account(name=f'{name} Transactions')

        try:
            # TODO: Put all this into a database transaction
            account = await self._database.accounts.create(account)
            wallet = Wallet(name, account=account)

            return await self._database.wallets.create(wallet)
        except Exception as error:
            raise CouldntCreateWallet(error)

    async def update(self, id, name=None):
        try:
            wallet = await self._database.wallets.find_by_id(id)
        except WalletDoesNotExist as error:
            raise WalletNotFound(id)
        
        wallet.name = name

        try:
            wallet = await self._database.wallets.update(wallet)
        except Exception as error:
            raise CouldntUpdateWallets(error)

        return wallet

    async def get_by_id(self, id):
        try:
           return await self._database.wallets.find_by_id(id)
        except WalletDoesNotExist as error:
            raise WalletNotFound(id)
        except Exception as error:
            raise CouldntGetWallets(error)

    async def get_list(self):
        try:
            wallets = await self._database.wallets.find_all()
        except Exception as error:
            raise CouldntGetWallets(error)

        return wallets
