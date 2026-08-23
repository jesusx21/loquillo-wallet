from sqlalchemy.ext.asyncio import AsyncEngine

from .accounts import account_fixtures
from .categories import category_fixtures
from .entries import entry_fixtures
from .transactions import transaction_fixtures
from .users import user_fixtures
from .wallets import wallet_fixtures

fixtures_mapped = {
    'accounts': account_fixtures,
    'categories': category_fixtures,
    'entries': entry_fixtures,
    'transactions': transaction_fixtures,
    'users': user_fixtures,
    'wallets': wallet_fixtures
}


async def load_fixtures(engine: AsyncEngine, *args: str):
    for fixture_name in args:
        fixture = fixtures_mapped[fixture_name]

        statement = fixture['table'] \
            .insert() \
            .values(fixture['data'])

        async with engine.begin() as connection:
            await connection.execute(statement)
