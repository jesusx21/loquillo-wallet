from .data import data, constants

from database import Database


async def load_fixtures(database: Database, store_names: list[str]):
    store_fixture_map = {
        'accounts': database.accounts,
        'wallets': database.wallets
    }

    for store_name in store_names:
        store = store_fixture_map[store_name]

        for item in data[store_name]:
            await store.create(item)

__all__ = ['load_fixtures', 'data', 'constants']
