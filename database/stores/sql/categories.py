from uuid import UUID

from .store import SQLStore
from database.stores.errors import NotFound, CategoryNotFound
from database.tables import Categories
from domain.entities import Category
from domain.entities.category import CategoryType


class SQLCategoriesStore(SQLStore):
    def __init__(self, database: object):
        super().__init__(database, Categories)

    async def create(self, category: Category):
        return await self._create(
            name=category.name,
            type=category.type.value,
            parent_category_id=category.parent_category_id,
            account_id=category.account_id,
            user_id=category.user_id
        )

    async def find_by_id(self, category_id: UUID) -> Category:
        try:
            return await self._find_by_id(category_id)
        except NotFound as error:
            raise CategoryNotFound(category_id) from error

    async def find_by_user_id(self, user_id: UUID) -> list[Category]:
        return await self._find(user_id=user_id)

    def _build_entity(self, **kwargs) -> Category:
        return Category(
            id=kwargs['id'],
            name=kwargs['name'],
            type=CategoryType(kwargs['type']),
            account_id=kwargs['account_id'],
            parent_category_id=kwargs['parent_category_id'],
            user_id=kwargs['user_id'],
            created_at=kwargs['created_at'],
            updated_at=kwargs['updated_at']
        )
