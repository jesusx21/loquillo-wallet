from uuid import uuid4

from tests.api import TestCase
from unittest.mock import patch

from database.stores.errors import DatabaseError


class TestGetWalletById(TestCase):
    def setUp(self):
        super().setUp()

        result = self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'cash'})

        self.wallet = result.json
        self.wallet_id = str(self.wallet['id'])

        self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'debit'})
        self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'credit'})

    def test_get_wallet_by_id(self):
        result = self.simulate_get(f'/MrKrabz/api/v1/wallets/{self.wallet_id}')

        self.assert_that(result.status_code).is_equal_to(200)
        self.assert_that(result.json).contains_only(
            'id', 'name', 'createdAt', 'updatedAt'
        )
        self.assert_that(result.json['id']).is_equal_to(self.wallet_id)
        self.assert_that(result.json['name']).is_equal_to(self.wallet['name'])

    def test_unexpected_error_on_invalid_id(self):
        result = self.simulate_get(f'/MrKrabz/api/v1/wallets/invalid-id')

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('INVALID_ID')

    def test_unexpected_error_on_unexistent_wallet(self):
        wallet_id = str(uuid4())
        result = self.simulate_get(f'/MrKrabz/api/v1/wallets/{wallet_id}')

        self.assert_that(result.status_code).is_equal_to(404)
        self.assert_that(result.json['code']).is_equal_to('WALLET_NOT_FOUND')

    def test_unexpected_error_on_database_failure(self):
        database = self.app.get_database()

        with patch.object(database.wallets, 'find_by_id') as mock:
            mock.side_effect = DatabaseError('An exception')

            result = self.simulate_get(f'/MrKrabz/api/v1/wallets/{self.wallet_id}')

            self.assert_that(result.status_code).is_equal_to(500)
            self.assert_that(result.json['code']).is_equal_to('UNEXPECTED_ERROR')
