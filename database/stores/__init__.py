from sqlalchemy.ext.asyncio import create_async_engine

from .errors import UnsupportedDatabaseDriverName
from .memory import InMemoryDatabase
from .sql import SQLDatabase
from app.config import Config

type Database = InMemoryDatabase | SQLDatabase


def get_database(config: Config) -> Database:
    if config.database_driver == 'sql':
        engine = create_async_engine(config.sql_connection_uri)

        return SQLDatabase(engine)
    if config.database_driver == 'memory':
        return InMemoryDatabase()

    raise UnsupportedDatabaseDriverName(config.database_driver)
