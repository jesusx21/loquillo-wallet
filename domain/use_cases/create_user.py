from database.stores import Database
from domain.crud import CRUD
from domain.entities import User
from domain.entities.wallet import WalletType
from domain.errors import CouldNotCreateUser


class CreateUser:
    def __init__(self, database: Database, crud: CRUD, names: str, last_names: str, email: str):
        self.__database = database
        self.__crud = crud

        self.__names = names
        self.__last_names = last_names
        self.__email = email

    async def execute(self):
        async with self.__database.transacting() as database:
            self.__database = database
            self.__crud.with_database(database)

            user = await self.__create_user()
            await self.__create_cash_wallet(user)

            await self.__create_income_categories(user)
            await self.__create_expense_categories(user)
            await self.__create_loan_categories(user)
            await self.__create_debt_categories(user)

            return user

    async def __create_user(self):
        user = User(
            names=self.__names,
            last_names=self.__last_names,
            email=self.__email
        )

        try:
            return await self.__database.users.create(user)
        except Exception as error:
            raise CouldNotCreateUser(cause=error) from error

    async def __create_cash_wallet(self, user):
        return await self.__crud.wallets.create(
            user_id=user.id,
            name='Efectivo',
            type=WalletType.CASH
        )

    async def __create_income_categories(self, user: User):
        categories_names = [
            'Ajuste Saldo', 'Bonos', 'Depositos', 'Devoluciones', 'Inversiones', 'Pagos',
            'Reembolsos', 'Regalos', 'Rendimientos', 'Retiros', 'Salario', 'Servicios',
            'Transferencias', 'Desconocido', 'Otros'
        ]

        for name in categories_names:
            await self.__crud.categories.create_income(user.id, name)

    async def __create_expense_categories(self, user: User):
        categories_names = [
            'Ahorros', 'Ajuste Saldo', 'Alquiler', 'Bebidas', 'Comida', 'Convivios', 'Deudas',
            'Educación', 'Entretenimiento', 'Impuestos', 'Pagos', 'Regalos', 'Ropa', 'Salud',
            'Servicios', 'Transferencias', 'Transporte', 'Desconocido', 'Otros'
        ]

        for name in categories_names:
            await self.__crud.categories.create_expense(user.id, name)

    async def __create_loan_categories(self, user: User):
        categories_names = ['Préstamo', 'Pago de Préstamo']

        for name in categories_names:
            await self.__crud.categories.create_loan(user.id, name)

    async def __create_debt_categories(self, user: User):
        categories_names = ['Deuda', 'Pago de Deuda']

        for name in categories_names:
            await self.__crud.categories.create_debt(user.id, name)
