from __future__ import annotations

from typing import TYPE_CHECKING

from .event import Event

if TYPE_CHECKING:
    from database import Database


class EventProcessor:
    def __init__(self, database: Database):
        self.__database = database

        self.__events = []
        self.__failed_events = []

    def add_event(self, event: Event):
        self.__events.append(event)

    async def process(self):
        while len(self.__events) > 0:
            event = self.__events.pop()

            try:
                await self.__process_event(event)
            except Exception as error:
                self.__failed_events.append((event, error))

    async def __process_event(self, event: Event):
        async with self.__database.transacting() as database:
            await event.process()

            for transaction in event.transactions:
                transaction_saved = await database.transactions.create(transaction)

                for entry in transaction.entries:
                    entry.transaction_id = transaction_saved.id
                    await database.entries.create(entry)
