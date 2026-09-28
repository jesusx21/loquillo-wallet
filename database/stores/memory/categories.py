from uuid import UUID

from database.stores.errors import NotFound, CategoryNotFound
from database.stores.memory.store import MemoryStore
from domain.entities.category import Category, CategoryType


class MemoryCategoriesStore(MemoryStore[Category]):
    async def find_by_id(self, id: UUID):
        try:
            return await super().find_by_id(id)
        except NotFound as error:
            raise CategoryNotFound(id) from error

    async def find_debt_by_user_id(self, user_id: UUID):
        return await self._find(CategoryType.DEBT, user_id)

    async def find_expense_by_user_id(self, user_id: UUID):
        return await self._find(CategoryType.EXPENSE, user_id)

    async def find_income_by_user_id(self, user_id: UUID):
        return await self._find(CategoryType.INCOME, user_id)

    async def find_loan_by_user_id(self, user_id: UUID):
        return await self._find(CategoryType.LOAN, user_id)

    async def find_by_user_id(self, user_id: UUID) -> list[Category]:
        return await self._find(user_id=user_id)
