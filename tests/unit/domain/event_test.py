from datetime import datetime
from uuid import uuid4

from tests import TestCase

from domain.core import Event
from domain.core.entity_accounts import EntityAccounts
from domain.core.event_processor import EventProcessor
from domain.core.posting_rule import PostingRule
from domain.entities import Entry, Transaction
from domain.entities.transaction import TransactionStatus
from domain.core.errors import (
    CouldNotLoadAccount,
    CouldNotLoadEventAccounts,
    CouldNotLoadEventEntities,
    ReadOnlyField
)


class DummyEvent(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transactions = []

    def get_metadata(self):
        return {
            'message': 'dummy event',
            'amount': 2500,
        }

    async def process(self):
        return None

    async def _load_entities(self, database):
        return None

    async def _load_accounts(self, database):
        return None


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

    def test_add_resulting_transaction_and_triggered_event(self):
        event = DummyEvent()
        transaction = object()
        triggered_event = DummyEvent()

        event.add_resulting_transaction(transaction)
        event.add_triggered_event(triggered_event)

        self.assert_that(event._resulting_transactions).is_equal_to([transaction])
        self.assert_that(event._triggered_events).is_equal_to([triggered_event])

    async def test_load_entities_marks_loaded_and_does_not_repeat(self):
        event = DummyEvent()

        await event.load_entities(self.get_database())

        self.assert_that(event._mark_entities_as_loaded).is_not_none()

    async def test_load_accounts_requires_entities_loaded(self):
        event = DummyEvent()

        with self.assertRaises(CouldNotLoadEventAccounts):
            await event.load_accounts(self.get_database())

    async def test_load_entities_wraps_errors(self):
        event = DummyEvent()

        async def raise_error(database):
            raise RuntimeError('boom')

        event._load_entities = raise_error

        with self.assertRaises(CouldNotLoadEventEntities):
            await event.load_entities(self.get_database())

    async def test_load_accounts_wraps_errors(self):
        event = DummyEvent()
        event._mark_entities_as_loaded()

        async def raise_error(database):
            raise RuntimeError('boom')

        event._load_accounts = raise_error

        with self.assertRaises(CouldNotLoadEventAccounts):
            await event.load_accounts(self.get_database())


class DummyProcessableEvent(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.processed = False
        self.transactions = [
            Transaction(
                description='Expense created by event processor',
                status=TransactionStatus.PENDING,
            )
        ]
        self.transactions[0].add_entries(
            Entry(account_id=uuid4(), amount=-50, concept='Groceries')
        )

    def get_metadata(self):
        return {'amount': 50}

    async def process(self):
        self.processed = True

    async def _load_entities(self, database):
        return None

    async def _load_accounts(self, database):
        return None


class FailingEvent(Event):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transactions = []

    def get_metadata(self):
        return {'amount': 0}

    async def process(self):
        raise RuntimeError('processor should catch this')

    async def _load_entities(self, database):
        return None

    async def _load_accounts(self, database):
        return None


class TestEventProcessor(TestCase):
    async def async_set_up(self):
        await super().async_set_up()
        self.database = self.get_database()

    async def test_processes_added_events(self):
        event = DummyProcessableEvent()
        processor = EventProcessor(self.database)

        processor.add_event(event)
        await processor.process()

        self.assert_that(event.processed).is_true()
        self.assert_that(processor._EventProcessor__failed_events).is_equal_to([])

    async def test_collects_failed_events(self):
        event = FailingEvent()
        processor = EventProcessor(self.database)

        processor.add_event(event)
        await processor.process()

        self.assert_that(len(processor._EventProcessor__failed_events)).is_equal_to(1)
        self.assert_that(processor._EventProcessor__failed_events[0][0]).is_equal_to(event)


class TestEntityAccounts(TestCase):
    async def test_find_by_account_id_returns_entries(self):
        expected = object()

        class Entries:
            async def find_by_account_id(self, account_id):
                return expected

        class Database:
            def __init__(self):
                self.entries = Entries()

        entity_accounts = EntityAccounts(Database())

        result = await entity_accounts.find_by_account_id(uuid4())

        self.assert_that(result).is_equal_to(expected)

    async def test_find_by_account_id_wraps_database_errors(self):
        class Entries:
            async def find_by_account_id(self, account_id):
                raise RuntimeError('database down')

        class Database:
            def __init__(self):
                self.entries = Entries()

        entity_accounts = EntityAccounts(Database())

        with self.assertRaises(CouldNotLoadAccount):
            await entity_accounts.find_by_account_id(uuid4())


class TestPostingRule(TestCase):
    def test_process_raises_not_implemented_error(self):
        rule = PostingRule()

        with self.assertRaisesRegex(NotImplementedError, 'DummyEvent'):
            rule.process(DummyEvent())
