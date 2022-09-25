from uuid import uuid4
from mister_krabz.entities import Category
from tests.api import TestCase
from unittest.mock import patch

from database.stores.errors import DatabaseError


class TestCreateSubcategories(TestCase):
    def setUp(self):
        super().setUp()

        self.database = self.get_database()
        self.parent_category = self.wait_for(
            self.database.categories.create(Category('Sale'))
        )

    def test_create_subcategory(self):
        payload = {'name': 'Bills'}
        result = self.simulate_post(
            f'/MrKrabz/api/v1/categories/{self.parent_category.id}/subcategories',
            json=payload
        )

        self.assert_that(result.status_code).is_equal_to(201)
        self.assert_that(result.json).contains_only(
            'id', 'name', 'createdAt', 'updatedAt'
        )
        self.assert_that(result.json['name']).is_equal_to('Bills')

    def test_return_error_on_invalid_id(self):
        payload = {'name': ''}
        result = self.simulate_post(
            f'/MrKrabz/api/v1/categories/invalid-id/subcategories',
            json=payload
        )

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('INVALID_ID')

    def test_return_error_on_empty_name(self):
        payload = {'name': ''}
        result = self.simulate_post(
            f'/MrKrabz/api/v1/categories/{self.parent_category.id}/subcategories',
            json=payload
        )

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('NAME_MISSING')

    def test_return_error_when_name_is_null(self):
        payload = {'name': None}
        result = self.simulate_post(
            f'/MrKrabz/api/v1/categories/{self.parent_category.id}/subcategories',
            json=payload
        )

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('NAME_MISSING')

    def test_return_error_when_parent_category_does_not_exist(self):
        payload = {'name': 'Sale'}
        result = self.simulate_post(
            f'/MrKrabz/api/v1/categories/{uuid4()}/subcategories',
            json=payload
        )

        self.assert_that(result.status_code).is_equal_to(404)
        self.assert_that(result.json['code']).is_equal_to('CATEGORY_NOT_FOUND')

    def test_unexpected_error_on_database_failure(self):
        database = self.app.get_database()

        with patch.object(database.categories, 'create') as mock:
            mock.side_effect = DatabaseError('An exception')

            payload = {'name': 'Bills'}
            result = self.simulate_post(
                f'/MrKrabz/api/v1/categories/{self.parent_category.id}/subcategories',
                json=payload
            )

            self.assert_that(result.status_code).is_equal_to(500)
            self.assert_that(result.json['code']).is_equal_to('UNEXPECTED_ERROR')
