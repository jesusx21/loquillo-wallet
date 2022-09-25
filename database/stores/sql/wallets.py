from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from database.tables import Wallets
from database.stores.errors import DatabaseError, InvalidId, WalletNotFound
from mister_krabz.core.wallet_account import WalletAccount
from mister_krabz.entities import Wallet


class WalletsStore:
    def __init__(self, db, engine):
        self._db = db
        self._engine = engine

    async def create(self, wallet):
        statement = Wallets \
            .insert() \
            .values(
                name=wallet.name,
                account_id=wallet._account.id
            ) \
            .returning('*')

        try:
            cursor = await self._execute(statement)

            return self._build_wallet(cursor.one())
        except Exception as error:
            raise DatabaseError(error)

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

            return self._build_wallet(cursor.one())
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

            return self._build_wallet(cursor.one())
        except NoResultFound as error:
            raise WalletNotFound(id) from error
        except Exception as error:
            raise DatabaseError(error)

    async def find_all(self):
        statement = Wallets \
            .select()

        try:
            cursor = await self._execute(statement)
            return self._build_wallets(cursor.all())
        except Exception as error:
            raise DatabaseError(error)

    def _build_wallet(self, result):
        data = dict(result)

        wallet = Wallet(
            id=data['id'],
            name=data['name'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )

        wallet.wallet_account = WalletAccount(self._db, wallet, data['account_id'])

        return wallet

    def _build_wallets(self, result):
        data = map(self._build_wallet, result)

        return list(data)

    async def _execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)
