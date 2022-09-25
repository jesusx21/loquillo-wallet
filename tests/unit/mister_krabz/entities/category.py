from uuid import uuid4
from mister_krabz.entities.category import CategoriesParentCategoriesAlreadySet

from tests import TestCase

from mister_krabz.core.categories_parent_categories import CategoriesParentCategories
from mister_krabz.entities import Category


class TestWallet(TestCase):
    async def asyncSetUp(self):
        await super().asyncSetUp()

        self.category = Category(name='Sales')
        self.db = self.get_database()
    
    def test_set_categories_parent_categories(self):
        self.category.set_categories_parent_categories(
            CategoriesParentCategories(self.db, category_id=uuid4(), parent_category_id=uuid4())
        )

        self.assert_that(self.category._categories_parent_categories).is_not_none()
    
    def test_error_when_setting_category_parent_category_already_set(self):
        self.category.set_categories_parent_categories(
            CategoriesParentCategories(self.db, category_id=uuid4(), parent_category_id=uuid4())
        )

        with self.assertRaises(CategoriesParentCategoriesAlreadySet):
            self.category.set_categories_parent_categories(
                CategoriesParentCategories(self.db, category_id=uuid4(), parent_category_id=uuid4())
            )

        


