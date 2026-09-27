from uuid import UUID

from database import Database
from domain.crud import CRUD
from domain.entities.wallet import Wallet, WalletType
from domain.errors import CouldNotCreateWallet


class CreateWallet:
    def __init__(self, database: Database, crud: CRUD, user_id: UUID, name: str, type: WalletType):
        self.__database = database
        self.__crud = crud

        self.__user_id = user_id
        self.__name = name
        self.__wallet_type = type

    async def execute(self):
        async with self.__database.transacting() as database:
            self.__crud.with_database(database)

            account = await self.__crud.accounts.create(f'Cuenta de {self.__name}')
            wallet = Wallet(
                name=self.__name,
                type=self.__wallet_type,
                account_id=account.id,
                user_id=self.__user_id
            )

            try:
                return await self.__database.wallets.create(wallet)
            except Exception as error:
                raise CouldNotCreateWallet(cause=error) from error
