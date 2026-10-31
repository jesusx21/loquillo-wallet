from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID

from .errors import CouldNotLoadWalletBalance

if TYPE_CHECKING:
    from database import Database


class WalletEntries:
    def __init__(self, database: Database, account_id: UUID):
        self._database = database
        self._account_id = account_id

    def __deepcopy__(self, memo):
        clone = WalletEntries(self._database, self._account_id)
        memo[id(self)] = clone

        return clone

    async def get_balance(self) -> int:
        try:
            return await self._database.entries.sum_by_account_id(self._account_id)
        except Exception as error:
            raise CouldNotLoadWalletBalance(self._account_id, cause=error) from error
