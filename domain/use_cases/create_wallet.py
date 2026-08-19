from uuid import UUID

from database import Database
from domain.use_cases.base_use_case import BaseUseCase
from domain.entities import DetailAccount
from domain.entities.wallet import Wallet, WalletType
from domain.errors import CouldNotCreateAccount, CouldNotCreateWallet


class CreateWallet(BaseUseCase):
    def __init__(self, database: Database, user_id: UUID, name: str, type: WalletType):
        super().__init__(database)

        self._user_id = user_id
        self._name = name
        self._wallet_type = type

    async def execute(self):
        async with self._execute_within_transaction():
            account = await self._create_account()
            wallet = Wallet(
                name=self._name,
                type=self._wallet_type,
                account_id=account.id,
                user_id=self._user_id
            )

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
