from uuid import UUID

from .create import CreateCategory
from .errors import CouldNotGetCategory, CategoryNotFound
from domain.crud.base import CRUDBase
from domain.entities.category import CategoryType
from database.stores.errors import CategoryNotFound as CategoryDoesNotExist


class Categories(CRUDBase):
    async def create_debt(self, user_id: UUID, name: str):
        return await self.__create_category(user_id, name, CategoryType.DEBT)

    async def create_expense(self, user_id: UUID, name: str):
        return await self.__create_category(user_id, name, CategoryType.EXPENSE)

    async def create_income(self, user_id: UUID, name: str):
        return await self.__create_category(user_id, name, CategoryType.INCOME)

    async def create_loan(self, user_id: UUID, name: str):
        return await self.__create_category(user_id, name, CategoryType.LOAN)

    async def get_by_id(self, category_id: UUID):
        try:
            return await self._database.categories.find_by_id(category_id)
        except CategoryDoesNotExist as error:
            raise CategoryNotFound(category_id) from error
        except Exception as error:
            raise CouldNotGetCategory(category_id, error) from error

    async def __create_category(self, user_id: UUID, name: str, type: CategoryType):
        create_category = CreateCategory(
            self._database,
            user_id,
            name,
            type,
        )

        return await create_category.execute()
