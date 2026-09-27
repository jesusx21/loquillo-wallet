from database.stores import Database
from domain.crud import CRUD
from domain.entities import User
from domain.entities.category import Category, CategoryType
from domain.entities.wallet import WalletType
from domain.errors import CouldNotCreateCategories, CouldNotCreateUser
from domain.use_cases.create_wallet import CreateWallet


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
        create_wallet = CreateWallet(
            database=self.__database,
            crud=self.__crud,
            user_id=user.id,
            name='Efectivo',
            type=WalletType.CASH
        )

        return await create_wallet.execute()

    def __build_category(self, user: User, name: str, type: CategoryType):
        category = Category(
            name=name,
            type=type,
            user_id=user.id
        )

        return category

    def __build_debt_category(self, user: User, name: str):
        return self.__build_category(user, name, type=CategoryType.DEBT)

    def __build_loan_category(self, user: User, name: str):
        return self.__build_category(user, name, type=CategoryType.LOAN)

    def __build_expense_category(self, user: User, name: str):
        return self.__build_category(user, name, type=CategoryType.EXPENSE)

    def __build_income_category(self, user: User, name: str):
        return self.__build_category(user, name, type=CategoryType.INCOME)

    async def __create_categories(self, categories: list[Category]):
        for category in categories:
            try:
                account = await self.__crud.accounts.create(f'Cuenta de {category.name}')
                category.account_id = account.id

                await self.__database.categories.create(category)
            except Exception as error:
                raise CouldNotCreateCategories(cause=error, category_name=category.name) from error

    async def __create_income_categories(self, user: User):
        categories = [
            self.__build_income_category(user, name='Ajuste Saldo'),
            self.__build_income_category(user, name='Bonos'),
            self.__build_income_category(user, name='Depositos'),
            self.__build_income_category(user, name='Devoluciones'),
            self.__build_income_category(user, name='Inversiones'),
            self.__build_income_category(user, name='Pagos'),
            self.__build_income_category(user, name='Reembolsos'),
            self.__build_income_category(user, name='Regalos'),
            self.__build_income_category(user, name='Rendimientos'),
            self.__build_income_category(user, name='Retiros'),
            self.__build_income_category(user, name='Salario'),
            self.__build_income_category(user, name='Servicios'),
            self.__build_income_category(user, name='Transferencias'),
            self.__build_income_category(user, name='Desconocido'),
            self.__build_income_category(user, name='Otros')
        ]

        await self.__create_categories(categories)

    async def __create_expense_categories(self, user: User):
        categories = [
            self.__build_expense_category(user, name='Ahorros'),
            self.__build_expense_category(user, name='Ajuste Saldo'),
            self.__build_expense_category(user, name='Alquiler'),
            self.__build_expense_category(user, name='Bebidas'),
            self.__build_expense_category(user, name='Comida'),
            self.__build_expense_category(user, name='Convivios'),
            self.__build_expense_category(user, name='Deudas'),
            self.__build_expense_category(user, name='Educación'),
            self.__build_expense_category(user, name='Entretenimiento'),
            self.__build_expense_category(user, name='Impuestos'),
            self.__build_expense_category(user, name='Pagos'),
            self.__build_expense_category(user, name='Regalos'),
            self.__build_expense_category(user, name='Ropa'),
            self.__build_expense_category(user, name='Salud'),
            self.__build_expense_category(user, name='Servicios'),
            self.__build_expense_category(user, name='Transferencias'),
            self.__build_expense_category(user, name='Transporte'),
            self.__build_expense_category(user, name='Desconocido'),
            self.__build_expense_category(user, name='Otros')
        ]

        await self.__create_categories(categories)

    async def __create_loan_categories(self, user: User):
        categories = [
            self.__build_loan_category(user, name='Préstamo'),
            self.__build_loan_category(user, name='Pago de Préstamo'),
        ]

        await self.__create_categories(categories)

    async def __create_debt_categories(self, user: User):
        categories = [
            self.__build_debt_category(user, name='Deuda'),
            self.__build_debt_category(user, name='Pago de Deuda'),
        ]

        await self.__create_categories(categories)
