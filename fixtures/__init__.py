from database.stores.memory import InMemoryDatabase

from domain.entities import DetailAccount
from .wallets import wallets

async def load_database(database: InMemoryDatabase):
    for wallet in wallets:
        account_name = f"{wallet.name} Account"
        account = await database.accounts.create(
            DetailAccount(account_name)
        )

        wallet.account = account
        await database.wallets.create(wallet)
