from tests.api import TestCase
from unittest.mock import patch

from database.stores.errors import DatabaseError


class TestWallets(TestCase):
    def test_create_wallet(self):
        payload = {'name': 'Debit'}
        result = self.simulate_post('/MrKrabz/api/v1/wallets', json=payload)

        self.assert_that(result.status_code).is_equal_to(201)
        self.assert_that(result.json).contains_only(
            'id', 'name', 'createdAt', 'updatedAt'
        )
        self.assert_that(result.json['name']).is_equal_to('Debit')

    def test_return_error_on_empty_name(self):
        payload = {'name': ''}
        result = self.simulate_post('/MrKrabz/api/v1/wallets', json=payload)

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('NAME_MISSING')

    def test_return_error_when_name_is_null(self):
        payload = {'name': None}
        result = self.simulate_post('/MrKrabz/api/v1/wallets', json=payload)

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('NAME_MISSING')

    def test_unexpected_error_on_database_failure(self):
        database = self.app.get_database()

        with patch.object(database.wallets, 'create') as mock:
            mock.side_effect = DatabaseError('An exception')

            payload = {'name': 'Debit'}
            result = self.simulate_post('/MrKrabz/api/v1/wallets', json=payload)

            self.assert_that(result.status_code).is_equal_to(500)
            self.assert_that(result.json['code']).is_equal_to('UNEXPECTED_ERROR')
