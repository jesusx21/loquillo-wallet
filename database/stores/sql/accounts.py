from datetime import datetime
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from database.tables import Accounts
from database.stores.errors import AccountNotFound, DatabaseError, InvalidId
from mister_krabz.entities.account import Account


class AccountsStore:
    def __init__(self, db, engine):
        self._db = db
        self._engine = engine

    async def create(self, account):
        statement = Accounts \
            .insert() \
            .values(name=account.name) \
            .returning('*')

        try:
            cursor = await self._execute(statement)

            return self._build_account(cursor.one())
        except Exception as error:
            raise DatabaseError(error)

    async def update(self, account):
        if not account.id:
            raise InvalidId(None)

        if not isinstance(account.id, UUID):
            raise InvalidId(account.id)

        statement = Accounts \
            .update() \
            .returning('*') \
            .where(Accounts.c.id == account.id) \
            .values(
                name=account.name,
                updated_at=datetime.now()
            )

        try:
            cursor = await self._execute(statement)

            return self._build_account(cursor.one())
        except NoResultFound as error:
            raise AccountNotFound(account.id) from error
        except Exception as error:
            raise DatabaseError(error)

    async def find_by_id(self, id):
        if not isinstance(id, UUID):
            raise InvalidId(id)
        
        statement = Accounts \
            .select() \
            .where(Accounts.c.id == id)
        
        try:
            cursor = await self._execute(statement)

            return self._build_account(cursor.one())
        except NoResultFound as error:
            raise AccountNotFound(id) from error
        except Exception as error:
            raise DatabaseError(error)

    def _build_account(self, result):
        data = dict(result)

        return Account(
            id=data['id'],
            name=data['name'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )

    async def _execute(self, statement):
        async with self._engine.begin() as connection:
            return await connection.execute(statement)
