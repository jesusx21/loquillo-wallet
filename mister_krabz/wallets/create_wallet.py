from mister_krabz.wallets.errors import CouldnCreateWallet


class CreateWallet:
    def __init__(self, database, name):
        self._database = database
        self._name = name

    async def run(self):
        try:
            wallet = await self._database.wallets.create(name=self._name)
        except Exception as error:
            raise CouldnCreateWallet(error)

        return wallet
