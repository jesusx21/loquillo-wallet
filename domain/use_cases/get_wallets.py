from uuid import UUID

from domain.errors import CouldNotGetWallets
from database import Database
from domain.entities.wallet import WalletType


class GetWallets:
    def __init__(self, database: Database, user_id: UUID, wallet_types: list[WalletType]):
        self._database = database
        self._user_id = user_id
        self._wallet_types = wallet_types

    async def execute(self):
        try:
            return await self._database.wallets.find(
                user_id=self._user_id,
                type=[wallet_type.value for wallet_type in self._wallet_types]
            )
        except Exception as error:
            raise CouldNotGetWallets(cause=error) from error
