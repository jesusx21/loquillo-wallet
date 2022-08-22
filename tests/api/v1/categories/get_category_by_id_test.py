from uuid import uuid4

from tests.api import TestCase
from unittest.mock import patch

from database.stores.errors import DatabaseError


class TestGetCategoryById(TestCase):
    def setUp(self):
        super().setUp()

        result = self.simulate_post('/MrKrabz/api/v1/categories', json={'name': 'Bills'})

        self.category = result.json
        self.category_id = str(self.category['id'])

        self.simulate_post('/MrKrabz/api/v1/categories', json={'name': 'Sales'})
        self.simulate_post('/MrKrabz/api/v1/categories', json={'name': 'Shopping'})

    def test_get_category_by_id(self):
        result = self.simulate_get(f'/MrKrabz/api/v1/categories/{self.category_id}')

        self.assert_that(result.status_code).is_equal_to(200)
        self.assert_that(result.json).contains_only(
            'id', 'name', 'createdAt', 'updatedAt'
        )
        self.assert_that(result.json['id']).is_equal_to(self.category_id)
        self.assert_that(result.json['name']).is_equal_to(self.category['name'])

    def test_unexpected_error_on_invalid_id(self):
        result = self.simulate_get(f'/MrKrabz/api/v1/categories/invalid-id')

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('INVALID_ID')

    def test_unexpected_error_on_unexistent_category(self):
        category_id = str(uuid4())
        result = self.simulate_get(f'/MrKrabz/api/v1/categories/{category_id}')

        self.assert_that(result.status_code).is_equal_to(404)
        self.assert_that(result.json['code']).is_equal_to('CATEGORY_NOT_FOUND')

    def test_unexpected_error_on_database_failure(self):
        database = self.app.get_database()

        with patch.object(database.categories, 'find_by_id') as mock:
            mock.side_effect = DatabaseError('An exception')

            result = self.simulate_get(f'/MrKrabz/api/v1/categories/{self.category_id}')

            self.assert_that(result.status_code).is_equal_to(500)
            self.assert_that(result.json['code']).is_equal_to('UNEXPECTED_ERROR')
