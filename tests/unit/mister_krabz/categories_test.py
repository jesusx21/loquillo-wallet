from unittest.mock import patch
from uuid import uuid4
from tests import TestCase

from mister_krabz import Categories
from mister_krabz.errors import (
    CouldntCreateCategory,
    CouldntGetCategories,
    CategoryNotFound
)


class TestCategory(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.database = self.get_database()
        self.categories = Categories(self.database)

        self.category = await self.database.categories.create(name='Purchase')
        await self.database.categories.create(name='Transport')
        await self.database.categories.create(name='Bills')


class TestCreateCategory(TestCategory):
    async def test_create_category(self):
        category = await self.categories.create(name='Shopping')

        self.assert_that(category['id']).is_not_none()
        self.assert_that(category['name']).is_equal_to('Shopping')

    async def test_error_unexpected_when_creating_category(self):
        with patch.object(self.database.categories, 'create') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntCreateCategory):
                await self.categories.create(name='credit')


class TestGetCategoryById(TestCategory):
    async def test_get_category_by_id(self):
        category = await self.categories.get_by_id(self.category['id'])

        self.assert_that(category['id']).is_equal_to(self.category['id'])
        self.assert_that(category['name']).is_equal_to(self.category['name'])

    async def test_error_on_unexistent_category(self):
        with self.assertRaises(CategoryNotFound):
            await self.categories.get_by_id(uuid4())

    async def test_error_unexpected_when_creating_category(self):
        with patch.object(self.database.categories, 'find_by_id') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntGetCategories):
                await self.categories.get_by_id(self.category['id'])


class TestGetCategories(TestCategory):
    async def test_get_categories(self):
        categories = await self.categories.get_list()

        self.assert_that(categories).is_length(3)

        for category in categories:
            self.assert_that(category).contains_only(
                'id', 'name', 'created_at', 'updated_at'
            )

    async def test_error_unexpected_when_getting_categories(self):
        with patch.object(self.database.categories, 'find_all') as mock:
            mock.side_effect = Exception('error')

            with self.assertRaises(CouldntGetCategories):
                await self.categories.get_list()
