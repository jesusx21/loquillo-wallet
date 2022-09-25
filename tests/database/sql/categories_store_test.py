from uuid import uuid4

from unittest.mock import patch
from mister_krabz.entities import Category
from tests.database import TestCase

from database.stores.errors import CategoryNotFound, DatabaseError, InvalidId


class TestCategoriesStore(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()

        self.category = await self.create_category(self.database, name='Shopping')

        await self.create_category(self.database, name='bills')
        await self.create_category(self.database, name='travels')
        await self.create_category(self.database, name='savings')
        await self.create_category(self.database, name='transport')

    async def asyncTearDown(self):
        await super().asyncTearDown()


class TestCreateCategory(TestCategoriesStore):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.category = Category(name='Sales')

    async def test_create_category_with_wallet(self):
        category = await self.database.categories.create(self.category)

        self.assert_that(category.id).is_not_none()
        self.assert_that(category.name).is_equal_to(self.category.name)
        self.assert_that(category.created_at).is_not_none()
        self.assert_that(category.updated_at).is_not_none()

    async def test_error_on_creating_category(self):
        with patch.object(self.database.categories, '_execute') as mock:
            mock.side_effect = Exception()

            with self.assertRaises(DatabaseError):
                await self.database.categories.create(self.category)


class TestFindCategoryById(TestCategoriesStore):
    async def test_find_by_id(self):
        category = await self.database.categories.find_by_id(self.category.id)

        self.assert_that(category.id).is_equal_to(self.category.id)
        self.assert_that(category.name).is_equal_to(self.category.name)
        self.assert_that(category.created_at).is_equal_to(self.category.created_at)
        self.assert_that(category.updated_at).is_equal_to(self.category.updated_at)

    async def test_raise_error_when_category_does_not_exist(self):
        with self.assertRaises(CategoryNotFound):
            await self.database.categories.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.categories.find_by_id('invalid-id')

    async def test_raise_error_on_finding_category_by_id(self):
        with patch.object(self.database.categories, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.categories.find_by_id(self.category.id)


class TestFindAll(TestCategoriesStore):
    async def test_find_all_categories(self):
        categories = await self.database.categories.find_all()

        self.assert_that(categories).is_length(5)

    async def test_raise_error_on_finding_categories(self):
        with patch.object(self.database.categories, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.categories.find_all()
