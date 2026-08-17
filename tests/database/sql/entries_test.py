from unittest.mock import patch
from uuid import UUID, uuid4

from . import SQLTestCase
from .fixtures import constants, load_fixtures

from database.stores.errors import DatabaseError, EntryNotFound, InvalidId
from domain.entities.entry import Entry


class TestEntriesStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

        await load_fixtures(self.engine, 'accounts', 'transactions')

    async def async_tear_down(self):
        await super().async_tear_down()


class TestCreateEntry(TestEntriesStore):
    async def async_set_up(self):
        await super().async_set_up()

        self.account = await self.database.accounts.find_by_id(constants.ALBO_ACCOUNT_ID)
        self.transaction = await self.database.transactions.find_by_id(constants.TRANSACTION_ID)

    async def test_create_entry(self):
        entry_to_create = Entry(
            account_id=self.account.id,
            concept='Coffee',
            amount=-150,
            transaction_id=constants.TRANSACTION_ID
        )

        entry = await self.database.entries.create(entry_to_create)

        self.assert_that(entry).is_instance_of(Entry)
        self.assert_that(entry.id).is_instance_of(UUID)
        self.assert_that(entry.account_id).is_equal_to(constants.ALBO_ACCOUNT_ID)
        self.assert_that(entry.concept).is_equal_to('Coffee')
        self.assert_that(entry.amount).is_equal_to(-150)
        self.assert_that(entry.transaction_id).is_equal_to(constants.TRANSACTION_ID)
        self.assert_that(entry.created_at).is_not_none()
        self.assert_that(entry.updated_at).is_not_none()

    async def test_error_on_creating_entry(self):
        entry_to_create = Entry(
            account_id=self.account.id,
            concept='Coffee',
            amount=-150,
            transaction_id=constants.TRANSACTION_ID
        )

        with patch.object(self.database.entries, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.entries.create(entry_to_create)


class TestFindEntryById(TestEntriesStore):
    async def async_set_up(self):
        await super().async_set_up()

        await load_fixtures(self.engine, 'entries')

    async def test_find_by_id(self):
        entry = await self.database.entries.find_by_id(constants.SOURCE_ENTRY_ID)

        self.assert_that(entry).is_instance_of(Entry)
        self.assert_that(entry.account_id).is_equal_to(constants.ALBO_ACCOUNT_ID)
        self.assert_that(entry.concept).is_equal_to('Groceries')
        self.assert_that(entry.amount).is_equal_to(-2500)

    async def test_raise_error_when_entry_does_not_exist(self):
        with self.assertRaises(EntryNotFound):
            await self.database.entries.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.entries.find_by_id('invalid-id')

    async def test_raise_error_on_finding_entry_by_id(self):
        with patch.object(self.database.entries, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.entries.find_by_id(constants.TARGET_ENTRY_ID)
