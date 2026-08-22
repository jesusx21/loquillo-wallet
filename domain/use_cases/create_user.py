from database.stores import Database
from domain.entities import Account, LoquilloWallet, User
from domain.entities.account import AccountType
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
            await self.__assign_loquillo_wallet(user)

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

    async def __assign_loquillo_wallet(self, user):
        incomes_account = await self.__create_account(name='Ingresos')
        expenses_account = await self.__create_account(name='Gastos')

        loquillo_wallet = LoquilloWallet(
            user_id=user.id,
            incomes_account_id=incomes_account.id,
            expenses_account_id=expenses_account.id
        )

        try:
            return await self._database.loquillo_wallets.create(loquillo_wallet)
        except Exception as error:
            raise CouldNotCreateUser(cause=error) from error

    async def __create_account(self, name: str):
        account = Account(
            name=name,
            type=AccountType.DETAIL
        )

        try:
            return await self._database.accounts.create(account)
        except Exception as error:
            raise CouldNotCreateUser(cause=error) from error
