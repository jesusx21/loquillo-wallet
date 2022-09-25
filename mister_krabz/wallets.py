from mister_krabz.entities import Wallet, WalletCategory
from mister_krabz.entities.account import Account
from database.stores.errors import (
    CategoryNotFound as CategoryDoesNotExist,
    WalletNotFound as WalletDoesNotExist
)
from mister_krabz.errors import (
    CategoryNotFound,
    CouldNotAddCategory,
    CouldntCreateWallet,
    CouldntGetWallets,
    CouldntUpdateWallets,
    WalletNotFound
)


class Wallets:
    def __init__(self, database):
        self._database = database
    
    async def add_category(self, wallet_id, category_id):
        try:
           wallet = await self._database.wallets.find_by_id(wallet_id)
        except WalletDoesNotExist:
            raise WalletNotFound(id)
        except Exception as error:
            raise CouldNotAddCategory(error)

        try:
            category = await self._database.categories.find_by_id(category_id)
        except CategoryDoesNotExist:
            raise CategoryNotFound(category_id)
        except Exception as error:
            raise CouldNotAddCategory(error)

        try:
            account = await self._database.accounts.create(
                Account(name=category.name)
            )
        except Exception as error:
            raise CouldNotAddCategory(error)

        wallet_category = WalletCategory(wallet, category, account)

        try:
            return await self._database.wallets.add_category(wallet_category)
        except Exception as error:
            raise CouldNotAddCategory(error)

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
        except WalletDoesNotExist:
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
    