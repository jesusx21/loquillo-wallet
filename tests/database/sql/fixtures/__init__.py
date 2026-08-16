from sqlalchemy.ext.asyncio import AsyncEngine


async def load_fixtures(engine: AsyncEngine, fixtures: list[dict[str, any]]):
    for fixture in fixtures:
        statement = fixture['table'] \
            .insert() \
            .values(fixture['data'])

        async with engine.begin() as connection:
            await connection.execute(statement)
