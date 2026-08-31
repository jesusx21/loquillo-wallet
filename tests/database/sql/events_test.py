from datetime import datetime
from unittest.mock import patch
from uuid import UUID, uuid4

from . import SQLTestCase

from database.stores.errors import DatabaseError, EventNotFound, InvalidId
from domain.core import Event


class DummyEvent(Event):
    def get_metadata(self):
        return {
            'message': 'dummy event',
            'amount': 2500,
        }


class TestEventsStore(SQLTestCase):
    async def async_set_up(self):
        await super().async_set_up()

        self.database = self.get_database()

    async def async_tear_down(self):
        await super().async_tear_down()


class TestCreateEvent(TestEventsStore):
    async def test_create_event(self):
        event_to_create = DummyEvent(
            date=datetime(2024, 1, 10),
            created_at=datetime(2024, 1, 10),
        )
        event_to_create.message = 'dummy event'
        event_to_create.amount = 2500

        event = await self.database.events.create(event_to_create)

        self.assert_that(event).is_instance_of(Event)
        self.assert_that(event.id).is_instance_of(UUID)
        self.assert_that(event.type).is_equal_to('Event')
        self.assert_that(event.date).is_equal_to(event_to_create.date)
        self.assert_that(event.created_at).is_equal_to(event_to_create.created_at)
        self.assert_that(event.message).is_equal_to('dummy event')
        self.assert_that(event.amount).is_equal_to(2500)

    async def test_error_on_creating_event(self):
        event_to_create = DummyEvent(
            date=datetime(2024, 1, 10),
            created_at=datetime(2024, 1, 10),
        )
        event_to_create.message = 'dummy event'
        event_to_create.amount = 2500

        with patch.object(self.database.events, '_execute') as mock:
            mock.side_effect = Exception('Database error')

            with self.assertRaises(DatabaseError):
                await self.database.events.create(event_to_create)


class TestFindEventById(TestEventsStore):
    async def async_set_up(self):
        await super().async_set_up()

        event_to_create = DummyEvent(
            date=datetime(2024, 1, 10),
            created_at=datetime(2024, 1, 10),
        )
        event_to_create.message = 'dummy event'
        event_to_create.amount = 2500

        self.event = await self.database.events.create(event_to_create)

    async def test_find_by_id(self):
        event = await self.database.events.find_by_id(self.event.id)

        self.assert_that(event).is_instance_of(Event)
        self.assert_that(event.id).is_equal_to(self.event.id)
        self.assert_that(event.type).is_equal_to('Event')
        self.assert_that(event.message).is_equal_to('dummy event')
        self.assert_that(event.amount).is_equal_to(2500)

    async def test_raise_error_when_event_does_not_exist(self):
        with self.assertRaises(EventNotFound):
            await self.database.events.find_by_id(uuid4())

    async def test_raise_error_when_id_is_invalid(self):
        with self.assertRaises(InvalidId):
            await self.database.events.find_by_id('invalid-id')

    async def test_raise_error_on_finding_event_by_id(self):
        with patch.object(self.database.events, '_execute') as mock:
            mock.side_effect = Exception('An exception')

            with self.assertRaises(DatabaseError):
                await self.database.events.find_by_id(self.event.id)
