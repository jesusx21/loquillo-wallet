from uuid import uuid4
from tests.api import TestCase


class TestAddCategory(TestCase):
    def setUp(self):
        super().setUp()

        self.database = self.get_database()
        self.wallet = self.wait_for(self.create_wallet(self.database, 'Cash'))
        self.category = self.wait_for(self.create_category(self.database, 'Sales'))

    def test_add_category(self):
        result = self.simulate_post(
            f'/MrKrabz/api/v1/wallets/{self.wallet.id}/categories/{self.category.id}/add',
        )

        self.assert_that(result.status_code).is_equal_to(201)
        self.assert_that(result.json).contains_only(
            'id', 'name', 'category', 'createdAt', 'updatedAt'
        )
        self.assert_that(result.json['name']).is_equal_to('Cash')
        self.assert_that(result.json['category']).contains_only('id', 'name')
        self.assert_that(result.json['category']['name']).is_equal_to('Sales')
    
    def test_return_error_when_wallet_id_is_invalid(self):
        result = self.simulate_post(
            f'/MrKrabz/api/v1/wallets/invalid-id/categories/{self.category.id}/add',
        )

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('INVALID_ID')
    
    def test_return_error_when_category_id_is_invalid(self):
        result = self.simulate_post(
            f'/MrKrabz/api/v1/wallets/{self.wallet.id}/categories/invalid-id/add',
        )

        self.assert_that(result.status_code).is_equal_to(400)
        self.assert_that(result.json['code']).is_equal_to('INVALID_ID')
    
    def test_return_error_when_wallet_does_not_exist(self):
        result = self.simulate_post(
            f'/MrKrabz/api/v1/wallets/{uuid4()}/categories/{self.category.id}/add',
        )

        self.assert_that(result.status_code).is_equal_to(404)
        self.assert_that(result.json['code']).is_equal_to('WALLET_NOT_FOUND')
    
    def test_return_error_when_wallet_does_not_exist(self):
        result = self.simulate_post(
            f'/MrKrabz/api/v1/wallets/{self.wallet.id}/categories/{uuid4()}/add',
        )

        self.assert_that(result.status_code).is_equal_to(404)
        self.assert_that(result.json['code']).is_equal_to('CATEGORY_NOT_FOUND')