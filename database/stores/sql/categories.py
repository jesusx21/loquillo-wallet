from uuid import UUID

from sqlalchemy.future import select

from sqlalchemy.exc import NoResultFound

from database.stores.errors import CategoryNotFound, DatabaseError, InvalidId
from database.tables import Categories
from mister_krabz.core.categories_parent_categories import CategoriesParentCategories
from mister_krabz.entities.category import Category


class CategoriesStore:
    def __init__(self, db, engine):
        self._db = db
        self._engine = engine

    async def create(self, category):
        parent_category_id = category._parent_category.id if category._parent_category else None

        statement = Categories \
            .insert() \
            .values(
                name=category.name,
                parent_category_id=parent_category_id
            ) \
            .returning('*')

        try:
            cursor = await self._execute(statement)

            return self._build_category(cursor.one())
        except Exception as error:
            raise DatabaseError(error)

    async def find_by_id(self, id):
        if not isinstance(id, UUID):
            raise InvalidId(id)
        
        statement = Categories \
            .select() \
            .where(Categories.c.id == id)
        
        try:
            cursor = await self._execute(statement)

            return self._build_category(cursor.one())
        except NoResultFound as error:
            raise CategoryNotFound(id) from error
        except Exception as error:
            raise DatabaseError(error)

    async def find_all(self):
        statement = Categories \
            .select()

        try:
            cursor = await self._execute(statement)
            return self._build_categories(cursor.all())
        except Exception as error:
            raise DatabaseError(error)

    def _build_category(self, result):
        data = dict(result)

        category = Category(
            id=data['id'],
            name=data['name'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )

        category.set_categories_parent_categories(
            CategoriesParentCategories(self._db, category.id, data['parent_category_id'])
        )

        return category

    def _build_categories(self, result):
        data = map(self._build_category, result)

        return list(data)

    async def _execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)