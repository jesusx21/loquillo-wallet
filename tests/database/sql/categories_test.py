from unittest.mock import patch
from uuid import UUID, uuid4

from tests.database.sql import SQLTestCase
from tests.database.sql.fixtures import constants, load_fixtures

from database.stores.errors import CategoryNotFound, DatabaseError, InvalidId
from domain.entities.category import Category, CategoryType


class TestCategoriesStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()
        await load_fixtures(self.engine, 'accounts', 'users', 'categories')


class TestCreateCategory(TestCategoriesStore):
    async def async_set_up(self):
        await super().async_set_up()

        self.category_to_create = Category(
            user_id=constants.SECOND_USER_ID,
            name='Nómina',
            type=CategoryType.INCOME,
            account_id=constants.ALBO_ACCOUNT_ID,
        )

    async def test_create_category(self):
        category = await self.database.categories.create(self.category_to_create)

        self.assert_that(category).is_instance_of(Category)
        self.assert_that(category.id).is_instance_of(UUID)
        self.assert_that(category.name).is_equal_to('Nómina')
        self.assert_that(category.type).is_equal_to(CategoryType.INCOME)
        self.assert_that(category.account_id).is_equal_to(constants.ALBO_ACCOUNT_ID)
        self.assert_that(category.user_id).is_equal_to(constants.SECOND_USER_ID)

    async def test_error_on_creating_category(self):
        with patch.object(self.database.categories, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.categories.create(self.category_to_create)


class TestFindCategoryById(TestCategoriesStore):
    async def test_find_by_id(self):
        category = await self.database.categories.find_by_id(constants.SALARY_CATEGORY_ID)

        self.assert_that(category).is_instance_of(Category)
        self.assert_that(category.id).is_equal_to(constants.SALARY_CATEGORY_ID)
        self.assert_that(category.name).is_equal_to('Salario')
        self.assert_that(category.type).is_equal_to(CategoryType.INCOME)
        self.assert_that(category.user_id).is_equal_to(constants.USER_ID)

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
                await self.database.categories.find_by_id(constants.SALARY_CATEGORY_ID)


class TestFindCategoriesByUserId(TestCategoriesStore):
    async def test_find_by_user_id(self):
        categories = await self.database.categories.find_by_user_id(constants.USER_ID)

        self.assert_that(categories).is_length(2)
        self.assert_that({category.name for category in categories}).is_equal_to({
            'Salario',
            'Alquiler'
        })
        self.assert_that({category.user_id for category in categories}).is_equal_to({
            constants.USER_ID
        })
