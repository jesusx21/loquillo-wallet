from database import Database
from domain.use_cases import CreateWallet
from run_script.fixtures.wallets import wallets


async def load_database(database: Database):
    for wallet_data in wallets:
        create_wallet = CreateWallet(database, **wallet_data)

        await create_wallet.execute()
