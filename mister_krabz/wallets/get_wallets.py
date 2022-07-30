from mister_krabz.wallets.errors import CouldnGetWallets


class GetWallets:
    def __init__(self, database):
        self._database = database

    async def run(self):
        try:
            wallets = await self._database.wallets.find_all()
        except Exception as error:
            raise CouldnGetWallets(error)

        return wallets
