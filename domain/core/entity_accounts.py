from __future__ import annotations
from uuid import UUID
from typing import TYPE_CHECKING

from domain.core.errors import CouldNotLoadAccount

if TYPE_CHECKING:
    from database import Database


class EntityAccounts:
    def __init__(self, database: Database):
        self.__database = database

    async def find_by_account_id(self, account_id: UUID):
        try:
            return await self.__database.entries.find_by_account_id(account_id)
        except Exception as error:
            raise CouldNotLoadAccount(account_id, cause=error) from error
