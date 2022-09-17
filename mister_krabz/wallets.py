from mister_krabz.errors import CouldntCreateWallet, CouldntGetWallets
from mister_krabz.entities import Wallet


class Wallets:
    def __init__(self, database):
        self._database = database

    async def create(self, name):
        wallet = Wallet(name=name)

        try:
            return await self._database.wallets.create(wallet)
        except Exception as error:
            raise CouldntCreateWallet(error)

    async def get_list(self):
        try:
            wallets = await self._database.wallets.find_all()
        except Exception as error:
            raise CouldntGetWallets(error)

        return wallets
