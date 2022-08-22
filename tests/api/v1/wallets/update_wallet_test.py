from uuid import uuid4

from tests.api import TestCase
from unittest.mock import patch

from database.stores.errors import DatabaseError


class TestUpdateWallet(TestCase):
    def setUp(self):
        super().setUp()

        result = self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'cash'})

        self.wallet_id = str(result.json['id'])

        self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'debit'})
        self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'credit'})

    def test_update_wallet(self):
        payload = {'name': 'Debit'}
        result = self.simulate_put(f'/MrKrabz/api/v1/wallets/{self.wallet_id}', json=payload)

        self.assert_that(result.status_code).is_equal_to(200)
        self.assert_that(result.json).contains_only(
            'id', 'name', 'createdAt', 'updatedAt'
        )
        self.assert_that(result.json['id']).is_equal_to(self.wallet_id)
        self.assert_that(result.json['name']).is_equal_to('Debit')

    def test_unexpected_error_on_invalid_id(self):
        payload = {'name': 'Debit'}
        result = self.simulate_put(f'/MrKrabz/api/v1/wallets/invalid-id', json=payload)

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('INVALID_ID')

    def test_unexpected_error_on_unexistent_wallet(self):
        payload = {'name': 'Debit'}
        wallet_id = str(uuid4())
        result = self.simulate_put(f'/MrKrabz/api/v1/wallets/{wallet_id}', json=payload)

        self.assert_that(result.status_code).is_equal_to(404)
        self.assert_that(result.json['code']).is_equal_to('WALLET_NOT_FOUND')

    def test_unexpected_error_on_database_failure(self):
        database = self.app.get_database()

        with patch.object(database.wallets, 'update') as mock:
            mock.side_effect = DatabaseError('An exception')

            payload = {'name': 'Debit'}
            result = self.simulate_put(f'/MrKrabz/api/v1/wallets/{self.wallet_id}', json=payload)

            self.assert_that(result.status_code).is_equal_to(500)
            self.assert_that(result.json['code']).is_equal_to('UNEXPECTED_ERROR')
