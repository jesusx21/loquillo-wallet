from tests.api import TestCase
from unittest.mock import patch

from database.stores.errors import DatabaseError


class TestGetWallets(TestCase):
    def setUp(self):
        super().setUp()

        self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'cash'})
        self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'debit'})
        self.simulate_post('/MrKrabz/api/v1/wallets', json={'name': 'credit'})

    def test_get_wallets(self):
        result = self.simulate_get('/MrKrabz/api/v1/wallets')

        self.assert_that(result.status_code).is_equal_to(200)
        self.assert_that(result.json).is_length(3)


        for wallet in result.json:
            self.assert_that(wallet).contains_only(
                'id', 'name', 'createdAt', 'updatedAt'
            )

    def test_unexpected_error_on_database_failure(self):
        database = self.app.get_database()

        with patch.object(database.wallets, 'find_all') as mock:
            mock.side_effect = DatabaseError('An exception')

            result = self.simulate_get('/MrKrabz/api/v1/wallets')

            self.assert_that(result.status_code).is_equal_to(500)
            self.assert_that(result.json['code']).is_equal_to('UNEXPECTED_ERROR')
