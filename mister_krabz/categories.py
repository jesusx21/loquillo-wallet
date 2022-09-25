from database.stores.errors import CategoryNotFound as CategoryDoesNotExist
from mister_krabz.entities import Category
from mister_krabz.errors import(
    CategoryNotFound,
    CouldntCreateCategory,
    CouldntGetCategories,
    ParentCategoryNotFound
)


class Categories:
    def __init__(self, database):
        self._database = database

    async def create(self, name, parent_category_id=None):
        parent_category = await self._get_parent_category(parent_category_id)
        category = Category(name, parent_category)

        try:
            category = await self._database.categories.create(category)
        except Exception as error:
            raise CouldntCreateCategory(error)

        return category

    async def get_by_id(self, id):
        try:
            category = await self._database.categories.find_by_id(id)
        except CategoryDoesNotExist as error:
            raise CategoryNotFound(id)
        except Exception as error:
            raise CouldntGetCategories(error)

        return category

    async def get_list(self):
        try:
            categories = await self._database.categories.find_all()
        except Exception as error:
            raise CouldntGetCategories(error)

        return categories
    
    async def _get_parent_category(self, parent_category_id):
        if not parent_category_id:
            return None
        
        try:
            return await self._database.categories.find_by_id(parent_category_id)
        except CategoryDoesNotExist as error:
            raise ParentCategoryNotFound(parent_category_id)
        except Exception as error:
            raise CouldntGetCategories(error)