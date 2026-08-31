from datetime import datetime
from uuid import uuid4

from tests import TestCase

from domain.core import Event
from domain.core.errors import ReadOnlyField


class DummyEvent(Event):
    def get_metadata(self):
        return {
            'message': 'dummy event',
            'amount': 2500,
        }


class TestEventEntity(TestCase):
    def test_event_type_uses_class_name(self):
        event = DummyEvent(
            date=datetime(2024, 1, 10),
            created_at=datetime(2024, 1, 10),
        )

        self.assert_that(event.type).is_equal_to('DummyEvent')

    def test_event_fields_are_read_only(self):
        event = Event(
            id=uuid4(),
            date=datetime(2024, 1, 10),
            created_at=datetime(2024, 1, 10),
        )

        with self.assertRaises(ReadOnlyField):
            event.id = uuid4()

        with self.assertRaises(ReadOnlyField):
            event.date = datetime(2024, 2, 10)

        with self.assertRaises(ReadOnlyField):
            event.created_at = datetime(2024, 2, 10)

    def test_get_metadata_must_be_implemented_by_subclass(self):
        event = Event()

        with self.assertRaises(NotImplementedError):
            event.get_metadata()
