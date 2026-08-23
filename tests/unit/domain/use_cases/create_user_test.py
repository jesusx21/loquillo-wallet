from uuid import UUID

from unittest.mock import patch

from tests import TestCase

from domain.entities import User
from domain.errors import CouldNotCreateUser
from domain.use_cases import CreateUser


class TestCreateUser(TestCase):
    def setUp(self):
        self.database = self.get_database()

        self.create_user = CreateUser(
            self.database,
            'Jon',
            'Doe',
            'jon.doe@example.com'
        )

    async def test_create_user(self):
        user = await self.create_user.execute()

        self.assert_that(user).is_instance_of(User)
        self.assert_that(user.id).is_instance_of(UUID)
        self.assert_that(user.names).is_equal_to('Jon')
        self.assert_that(user.last_names).is_equal_to('Doe')
        self.assert_that(user.email).is_equal_to('jon.doe@example.com')

    async def test_creates_cash_wallet_for_user(self):
        user = await self.create_user.execute()
        [wallet] = await self.database.wallets.find_by_user_id(user.id)

        self.assert_that(wallet).is_not_none()
        self.assert_that(wallet.user_id).is_equal_to(user.id)
        self.assert_that(wallet.name).is_equal_to('Efectivo')
        self.assert_that(wallet.type).is_equal_to('cash')

    async def test_raises_could_not_create_user_error(self):
        with patch.object(self.database.users, 'create') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(CouldNotCreateUser):
                await self.create_user.execute()
