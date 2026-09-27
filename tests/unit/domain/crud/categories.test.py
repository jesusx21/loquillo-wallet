from uuid import uuid4

from unittest.mock import patch

from tests import TestCase

from domain.entities import Account, Category
from domain.crud.categories import Categories
from domain.crud.categories.errors import (
  CategoryNotFound,
  CouldNotCreateCategory,
  CouldNotGetCategory
)


class TestCategoriesCRUD(TestCase):
    def set_up(self):
        self.database = self.get_database()

        self.categories = Categories(self.database)
        self.user_id = uuid4()


class TestCreateDebtCategory(TestCategoriesCRUD):
    async def test_create_debt(self):
        category = await self.categories.create_debt(self.user_id, 'Debt')

        self.assert_that(category).is_not_none()
        self.assert_that(category).is_instance_of(Category)
        self.assert_that(category.name).is_equal_to('Debt')
        self.assert_that(category.user_id).is_equal_to(self.user_id)
        self.assert_that(category.type.value).is_equal_to('debt')
        self.assert_that(category.id).is_not_none()
        self.assert_that(category.created_at).is_not_none()
        self.assert_that(category.updated_at).is_not_none()

    async def test_account_is_created_for_category(self):
        category = await self.categories.create_debt(self.user_id, 'Debt')

        account = await self.database.accounts.find_by_id(category.account_id)
        self.assert_that(account).is_not_none()
        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.id).is_equal_to(category.account_id)
        self.assert_that(account.name).is_equal_to('Cuenta de Debt')

    async def test_raise_error_when_database_fails(self):
        with patch.object(self.database.categories, 'create') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotCreateCategory):
                await self.categories.create_debt(self.user_id, 'Debt')


class TestCreateExpenseCategory(TestCategoriesCRUD):
    async def test_create_expense(self):
        category = await self.categories.create_expense(self.user_id, 'Expense')

        self.assert_that(category).is_not_none()
        self.assert_that(category).is_instance_of(Category)
        self.assert_that(category.name).is_equal_to('Expense')
        self.assert_that(category.user_id).is_equal_to(self.user_id)
        self.assert_that(category.type.value).is_equal_to('expense')
        self.assert_that(category.id).is_not_none()
        self.assert_that(category.created_at).is_not_none()
        self.assert_that(category.updated_at).is_not_none()

    async def test_account_is_created_for_category(self):
        category = await self.categories.create_expense(self.user_id, 'Expense')

        account = await self.database.accounts.find_by_id(category.account_id)
        self.assert_that(account).is_not_none()
        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.id).is_equal_to(category.account_id)
        self.assert_that(account.name).is_equal_to('Cuenta de Expense')

    async def test_raise_error_when_database_fails(self):
        with patch.object(self.database.categories, 'create') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotCreateCategory):
                await self.categories.create_expense(self.user_id, 'Expense')


class TestCreateIncomeCategory(TestCategoriesCRUD):
    async def test_create_income(self):
        category = await self.categories.create_income(self.user_id, 'Income')

        self.assert_that(category).is_not_none()
        self.assert_that(category).is_instance_of(Category)
        self.assert_that(category.name).is_equal_to('Income')
        self.assert_that(category.user_id).is_equal_to(self.user_id)
        self.assert_that(category.type.value).is_equal_to('income')
        self.assert_that(category.id).is_not_none()
        self.assert_that(category.created_at).is_not_none()
        self.assert_that(category.updated_at).is_not_none()

    async def test_account_is_created_for_category(self):
        category = await self.categories.create_income(self.user_id, 'Income')

        account = await self.database.accounts.find_by_id(category.account_id)
        self.assert_that(account).is_not_none()
        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.id).is_equal_to(category.account_id)
        self.assert_that(account.name).is_equal_to('Cuenta de Income')

    async def test_raise_error_when_database_fails(self):
        with patch.object(self.database.categories, 'create') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotCreateCategory):
                await self.categories.create_income(self.user_id, 'Income')


class TestCreateLoanCategory(TestCategoriesCRUD):
    async def test_create_loan(self):
        category = await self.categories.create_loan(self.user_id, 'Loan')

        self.assert_that(category).is_not_none()
        self.assert_that(category).is_instance_of(Category)
        self.assert_that(category.name).is_equal_to('Debt')
        self.assert_that(category.user_id).is_equal_to(self.user_id)
        self.assert_that(category.type).is_equal_to('debt')
        self.assert_that(category.id).is_not_none()
        self.assert_that(category.created_at).is_not_none()
        self.assert_that(category.updated_at).is_not_none()

    async def test_account_is_created_for_category(self):
        category = await self.categories.create_loan(self.user_id, 'Loan')

        account = await self.database.accounts.find_by_id(category.account_id)
        self.assert_that(account).is_not_none()
        self.assert_that(account).is_instance_of(Account)
        self.assert_that(account.id).is_equal_to(category.account_id)
        self.assert_that(account.name).is_equal_to('Cuenta de Loan')

    async def test_raise_error_when_database_fails(self):
        with patch.object(self.database.categories, 'create') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotCreateCategory):
                await self.categories.create_loan(self.user_id, 'Loan')


class TestGetCategoryById(TestCategoriesCRUD):
    async def async_set_up(self):
        await super().async_set_up()

        self.category = await self.categories.create_income(self.user_id, 'Income')

    async def test_get_by_id(self):
        category = await self.categories.get_by_id(self.category.id)

        self.assert_that(category).is_not_none()
        self.assert_that(category).is_instance_of(Category)
        self.assert_that(category.id).is_equal_to(self.category.id)
        self.assert_that(category.name).is_equal_to('Income')
        self.assert_that(category.user_id).is_equal_to(self.category.user_id)
        self.assert_that(category.type.value).is_equal_to('income')
        self.assert_that(category.created_at).is_equal_to(self.category.created_at)
        self.assert_that(category.updated_at).is_equal_to(self.category.updated_at)

    async def test_raise_error_when_category_not_found(self):
        with self.assertRaises(CategoryNotFound):
            await self.categories.get_by_id(uuid4())

    async def test_raise_error_when_database_fails(self):
        with patch.object(self.database.categories, 'find_by_id') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotGetCategory):
                await self.categories.get_by_id(self.category.id)
