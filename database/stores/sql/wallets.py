from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from database.tables import Wallets
from database.stores.errors import DatabaseError, InvalidId, WalletNotFound
from mister_krabz.entities import Wallet


class WalletsStore:
    def __init__(self, engine):
        self._engine = engine

    async def create(self, wallet):
        statement = Wallets \
            .insert() \
            .values(name=wallet.name)

        try:
            cursor = await self._execute(statement)
        except Exception as error:
            raise DatabaseError(error)

        return await self.find_by_id(cursor.inserted_primary_key[0])

    async def update(self, wallet):
        if not wallet.id:
            raise InvalidId(None)

        if not isinstance(wallet.id, UUID):
            raise InvalidId(wallet.id)

        statement = Wallets \
            .update() \
            .returning('*') \
            .where(Wallets.c.id == wallet.id) \
            .values(
                name=wallet.name,
                updated_at=datetime.now()
            )

        try:
            cursor = await self._execute(statement)

            return self.build_wallet(cursor.one())
        except NoResultFound as error:
            raise WalletNotFound(wallet.id) from error
        except Exception as error:
            raise DatabaseError(error)


    async def find_by_id(self, id):
        if not isinstance(id, UUID):
            raise InvalidId(id)

        statement = Wallets \
            .select() \
            .where(Wallets.c.id == id)

        try:
            cursor = await self._execute(statement)

            return self.build_wallet(cursor.one())
        except NoResultFound as error:
            raise WalletNotFound(id) from error
        except Exception as error:
            raise DatabaseError(error)

    async def find_all(self):
        statement = Wallets \
            .select()

        try:
            cursor = await self._execute(statement)
            return self.build_wallets(cursor.all())
        except Exception as error:
            raise DatabaseError(error)

    def build_wallet(self, result):
        data = dict(result)

        return Wallet(
            id=data['id'],
            name=data['name'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )

    def build_wallets(self, result):
        data = map(self.build_wallet, result)

        return list(data)

    async def _execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)
