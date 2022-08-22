from uuid import uuid4

from unittest.mock import patch
from tests.database import TestCase

from database.stores.errors import CategoryNotFound, DatabaseError, InvalidId


class TestCategoriesStore(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()
        self.wallet = await self.database.wallets.create(name='cash')
        self.second_wallet = await self.database.wallets.create(name='cash')
        self.wallet_without_categories = await self.database.wallets.create(name='credit')
        self.category = await self.database.categories.create(name='Shopping', wallet=self.wallet)

        await self.database.categories.create(name='bills', wallet=self.wallet)
        await self.database.categories.create(name='travels', wallet=self.wallet)
        await self.database.categories.create(name='savings', wallet=self.second_wallet)
        await self.database.categories.create(name='transport')

    async def asyncTearDown(self):
        await super().asyncTearDown()


class TestCreateCategory(TestCategoriesStore):
    async def test_create_category_with_wallet(self):
        category = await self.database.categories.create(name='Sales', wallet=self.wallet)

        self.assert_that(category['id']).is_not_none()
        self.assert_that(category['name']).is_equal_to('Sales')
        self.assert_that(category['wallet_id']).is_equal_to(self.wallet['id'])

    async def test_create_category_without_wallet(self):
        category = await self.database.categories.create(name='Sales')

        self.assert_that(category['id']).is_not_none()
        self.assert_that(category['name']).is_equal_to('Sales')
        self.assert_that(category['wallet_id']).is_none()

    async def test_error_on_creating_category(self):
        with patch.object(self.database.categories._store, 'execute') as mock:
            mock.side_effect = Exception()

            with self.assertRaises(DatabaseError):
                await self.database.categories.create(name='Sales', wallet=self.wallet)


class TestFindCategoryById(TestCategoriesStore):
    async def test_find_by_id(self):
        category = await self.database.categories.find_by_id(self.category['id'])

        self.assert_that(category['id']).is_equal_to(self.category['id'])
        self.assert_that(category['name']).is_equal_to(self.category['name'])
        self.assert_that(category['created_at']).is_equal_to(self.category['created_at'])
        self.assert_that(category['updated_at']).is_equal_to(self.category['updated_at'])

    async def test_raise_error_when_category_does_not_exist(self):
        with self.assertRaises(CategoryNotFound):
            await self.database.categories.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.categories.find_by_id('invalid-id')

    async def test_raise_error_on_finding_category_by_id(self):
        with patch.object(self.database.categories._store, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.categories.find_by_id(self.category['id'])


class TestFindCategoriesByWalletId(TestCategoriesStore):
    async def test_find_categories_by_wallet_id(self):
        categories = await self.database.categories.find_by_wallet_id(self.wallet['id'])

        self.assert_that(categories).is_length(3)

        for category in categories:
            self.assert_that(category['wallet_id']).is_equal_to(self.wallet['id'])
            self.assert_that(category).contains_only(
                'id', 'name', 'wallet_id', 'created_at', 'updated_at'
            )

    async def test_return_empty_list_when_wallet_has_not_categories(self):
        categories = await self.database \
            .categories \
            .find_by_wallet_id(self.wallet_without_categories['id'])

        self.assert_that(categories).is_length(0)

    async def test_raise_error_on_finding_categories_by_wallet_id(self):
        with patch.object(self.database.categories._store, 'execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.categories.find_by_wallet_id(self.wallet['id'])
