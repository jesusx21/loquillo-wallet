from mister_krabz.entities import Wallet
from mister_krabz.wallets.errors import CouldnCreateWallet


class CreateWallet:
    def __init__(self, database, name):
        self._database = database
        self._wallet = Wallet(name=name)

    async def run(self):
        try:
            wallet = await self._database.wallets.create(self._wallet)
        except Exception as error:
            raise CouldnCreateWallet(error)

        return wallet
