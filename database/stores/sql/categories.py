from uuid import UUID

from sqlalchemy.future import select

from database.stores.errors import CategoryNotFound, DatabaseError, InvalidId, NotFound
from database.stores.sql.store import SQLStore
from database.tables import Categories, WalletsCategories


class CategoriesStore:
    def __init__(self, engine):
        self._store = SQLStore(engine, table=Categories)

    async def create(self, name, wallet=None):
        category = await self._store.create(name=name)

        if wallet:
            await self._link_category_to_wallet(category['id'], wallet['id'])
            category['wallet_id'] = wallet['id']
        else:
            category['wallet_id'] = None

        return category

    async def find_by_id(self, id):
        try:
            return await self._store.find_by_id(id)
        except NotFound:
            raise CategoryNotFound(id)

    def find_all(self):
        return self._store.find_list()

    def find_by_wallet_id(self, wallet_id):
        statement = select(
            Categories.c.id,
            Categories.c.name,
            WalletsCategories.c.wallet_id,
            Categories.c.created_at,
            Categories.c.updated_at
        ) \
            .join(
                WalletsCategories,
                WalletsCategories.c.category_id == Categories.c.id
            ) \
            .where(WalletsCategories.c.wallet_id == wallet_id)

        return self._store.find_list(statement=statement)


    async def _link_category_to_wallet(self, category_id, wallet_id):
        statement = WalletsCategories \
            .insert() \
            .values(
                category_id=category_id,
                wallet_id=wallet_id
            ) \
            .returning('*')

        try:
            cursor = await self._store.execute(statement)
        except Exception as error:
            raise DatabaseError(error)

        return dict(cursor.one())
