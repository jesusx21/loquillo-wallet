from uuid import uuid4

from tests import TestCase

from domain.crud import CRUD
from domain.entities.category import CategoryType
from domain.use_cases import GetCategories


class TestGetCategories(TestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()
        self.crud = CRUD(self.database)

        self.user_id = uuid4()
        self.income = await self.crud.categories.create_income(self.user_id, 'Salary')
        self.expense = await self.crud.categories.create_expense(self.user_id, 'Rent')

    async def test_get_categories_by_name(self):
        get_categories = GetCategories(self.crud, self.user_id, q='sal')
        categories = await get_categories.execute()

        self.assert_that(categories).is_length(1)
        self.assert_that(categories[0].id).is_equal_to(self.income.id)

    async def test_get_categories_by_type(self):
        get_categories = GetCategories(self.crud, self.user_id, type=CategoryType.EXPENSE)
        categories = await get_categories.execute()

        self.assert_that(categories).is_length(1)
        self.assert_that(categories[0].id).is_equal_to(self.expense.id)

    async def test_get_all_categories(self):
        get_categories = GetCategories(self.crud, self.user_id)
        categories = await get_categories.execute()

        self.assert_that(categories).is_length(2)

    async def test_does_not_get_categories_from_other_users(self):
        get_categories = GetCategories(self.crud, uuid4())
        categories = await get_categories.execute()

        self.assert_that(categories).is_empty()
