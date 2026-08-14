from database.stores.memory import InMemoryDatabase
from domain.entities import DetailAccount
from domain.entities.wallet import Wallet, WalletType
from domain.errors import CouldNotCreateAccount, CouldNotCreateWallet


class CreateWallet:
    def __init__(self, database: InMemoryDatabase, name: str, type: WalletType):
        self._database = database
        self._name = name
        self._wallet_type = type

    async def execute(self):
        account = await self._create_account()
        wallet = Wallet(self._name, self._wallet_type, account)

        try:
            return await self._database.wallets.create(wallet)
        except Exception as error:
            raise CouldNotCreateWallet(cause=error) from error

    async def _create_account(self):
        try:
            account = DetailAccount(f'{self._name} Account')
            return await self._database.accounts.create(account)
        except Exception as error:
            raise CouldNotCreateAccount(cause=error) from error
