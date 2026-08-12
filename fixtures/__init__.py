from database.stores.memory import InMemoryDatabase

from .accounts import accounts

async def load_database(database: InMemoryDatabase):
    for account in accounts:
        await database.accounts.create(account)
