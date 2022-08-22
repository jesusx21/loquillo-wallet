from database.stores.errors import InvalidId, NotFound, AccountNotFound
from database.stores.memory.store import MemoryStore


class AccountsStore:
    def __init__(self):
        self._store = MemoryStore()

    def create(self, name, wallet):
        return self._store.create(name=name, wallet_id=wallet['id'])

    async def update(self, data):
        if 'id' not in data:
            raise InvalidId(None)

        account = await self.find_by_id(data['id'])
        account['name'] = data['name']

        try:
            return await self._store.update(account)
        except NotFound:
            raise AccountNotFound(data['id'])

    async def find_by_id(self, id):
        try:
            return await self._store.find_by_id(id)
        except NotFound:
            raise AccountNotFound(id)

    def find_by_wallet_id(self, wallet_id):
        def filter_by_wallet_id(account):
            return account['wallet_id'] == wallet_id

        return self._store.find_list(filter_by_wallet_id)
