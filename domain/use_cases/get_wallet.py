from uuid import UUID

from domain.crud import CRUD


class GetWallet:
    def __init__(self, crud: CRUD, wallet_id: UUID):
        self.__crud = crud
        self.__wallet_id = wallet_id

    async def execute(self):
        return await self.__crud.wallets.get_by_id(self.__wallet_id)
