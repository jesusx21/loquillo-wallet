from database.stores import Database
from domain.entities import User
from domain.entities.wallet import WalletType
from domain.errors import CouldNotCreateUser
from domain.use_cases.base_use_case import BaseUseCase
from domain.use_cases.create_wallet import CreateWallet


class CreateUser(BaseUseCase):
    def __init__(self, database: Database, names: str, last_names: str, email: str):
        super().__init__(database)

        self.__names = names
        self.__last_names = last_names
        self.__email = email

    async def execute(self):
        async with self._execute_within_transaction():
            user = await self.__create_user()
            await self.__create_cash_wallet(user)

            return user

    async def __create_user(self):
        user = User(
            names=self.__names,
            last_names=self.__last_names,
            email=self.__email
        )

        try:
            return await self._database.users.create(user)
        except Exception as error:
            raise CouldNotCreateUser(cause=error) from error

    async def __create_cash_wallet(self, user):
        create_wallet = CreateWallet(
            database=self._database,
            user_id=user.id,
            name='Efectivo',
            type=WalletType.CASH
        )

        return await create_wallet.execute()
