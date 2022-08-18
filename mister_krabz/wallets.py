from mister_krabz.errors import CouldntCreateWallet, CouldntGetWallets


class Wallets:
    def __init__(self, database):
        self._database = database

    async def create(self, name):
        try:
            wallet = await self._database.wallets.create(name=name)
        except Exception as error:
            raise CouldntCreateWallet(error)

        return wallet

    async def get_list(self):
        try:
            wallets = await self._database.wallets.find_all()
        except Exception as error:
            raise CouldntGetWallets(error)

        return wallets
