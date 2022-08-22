from database.stores.sql.store import SQLStore

from database.tables import Accounts
from database.stores.errors import AccountNotFound, InvalidId, NotFound


class AccountsStore:
    def __init__(self, engine):
        self._store = SQLStore(engine, table=Accounts)

    def create(self, name, wallet):
        return self._store.create(name=name, wallet_id=wallet['id'])

    async def update(self, account):
        if 'id' not in account:
            raise InvalidId(None)

        try:
            return await self._store.update(
                id=account['id'],
                name=account['name']
            )
        except NotFound:
            raise AccountNotFound(account['id'])

    async def find_by_id(self, id):
        try:
            return await self._store.find_by_id(id)
        except NotFound:
            raise AccountNotFound(id)

    def find_by_wallet_id(self, wallet_id):
        return self._store.find_list(Accounts.c.wallet_id == wallet_id)
