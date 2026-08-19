from contextlib import asynccontextmanager

from database.stores import Database


class BaseUseCase:
    def __init__(self, database: Database):
        self._database = database

    @asynccontextmanager
    async def _execute_within_transaction(self):
        if self._database.is_transacting():
            yield
            return

        async with self._database.transacting() as database:
            self._database = database
            yield
