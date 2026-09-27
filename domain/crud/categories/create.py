from uuid import UUID

from .errors import CouldNotCreateCategory
from database.stores import Database
from domain.crud.accounts import Accounts
from domain.entities.category import Category, CategoryType


class CreateCategory:
    def __init__(self, database: Database, user_id: UUID, name: str, type: CategoryType):
        self.__database = database
        self.__accounts = Accounts(database)

        self.__name = name
        self.__type = type
        self.__user_id = user_id

    async def execute(self):
        account = await self.__accounts.create(f'Cuenta de {self.__name}')
        category = Category(
            name=self.__name,
            type=self.__type,
            account_id=account.id,
            user_id=self.__user_id,
        )

        try:
            return await self.__database.categories.create(category)
        except Exception as error:
            raise CouldNotCreateCategory(cause=error) from error
