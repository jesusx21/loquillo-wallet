from uuid import UUID

from database import Database
from domain.crud import CRUD
from domain.entities.wallet import WalletType


class CreateWallet:
    def __init__(self, database: Database, crud: CRUD, user_id: UUID, name: str, type: WalletType):
        self.__database = database
        self.__crud = crud

        self.__user_id = user_id
        self.__name = name
        self.__wallet_type = type

    async def execute(self):
        async with self.__database.transacting() as database:
            self.__crud.with_database(database)

            return self.__crud.wallets.create(
                self.__user_id,
                self.__name,
                self.__wallet_type
            )
