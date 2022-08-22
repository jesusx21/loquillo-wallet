from database.stores.errors import CategoryNotFound as CategoryDoesNotExist
from mister_krabz.errors import CategoryNotFound, CouldntCreateCategory, CouldntGetCategories


class Categories:
    def __init__(self, database):
        self._database = database

    async def create(self, name):
        try:
            category = await self._database.categories.create(name)
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
