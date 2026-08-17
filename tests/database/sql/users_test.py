from uuid import UUID, uuid4

from unittest.mock import patch

from tests.database.sql import SQLTestCase
from .fixtures import constants, load_fixtures

from database.stores.errors import DatabaseError, InvalidId, UserNotFound
from domain.entities.user import User


class TestUsersStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

    async def async_tear_down(self):
        await super().async_tear_down()


class TestCreateUser(TestUsersStore):
    async def async_set_up(self):
        await super().async_set_up()

        self.user_to_create = User(
            names='Leslie',
            last_names='Knope',
            email='leslie@pawne.com'
        )

    async def test_create_user(self):
        user = await self.database.users.create(self.user_to_create)

        self.assert_that(user).is_instance_of(User)
        self.assert_that(user.id).is_instance_of(UUID)
        self.assert_that(user.names).is_equal_to('Leslie')
        self.assert_that(user.last_names).is_equal_to('Knope')
        self.assert_that(user.email).is_equal_to('leslie@pawne.com')
        self.assert_that(user.created_at).is_not_none()
        self.assert_that(user.updated_at).is_not_none()

    async def test_error_on_creating_user(self):
        with patch.object(self.database.users, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.users.create(self.user_to_create)


class TestFindUserById(TestUsersStore):
    async def async_set_up(self):
        await super().async_set_up()

        await load_fixtures(self.engine, 'users')

    async def test_find_by_id(self):
        user = await self.database.users.find_by_id(constants.USER_ID)

        self.assert_that(user).is_instance_of(User)
        self.assert_that(user.id).is_equal_to(constants.USER_ID)
        self.assert_that(user.names).is_equal_to('Jon')
        self.assert_that(user.last_names).is_equal_to('Doe')
        self.assert_that(user.email).is_equal_to('jon.doe@example.com')

    async def test_raise_error_when_user_does_not_exist(self):
        with self.assertRaises(UserNotFound):
            await self.database.users.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.users.find_by_id('invalid-id')

    async def test_raise_error_on_finding_user_by_id(self):
        with patch.object(self.database.users, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.users.find_by_id(constants.USER_ID)
