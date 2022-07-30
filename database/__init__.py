from sqlalchemy.ext.asyncio import create_async_engine

from database.stores.sql import SQLDatabase


class UnsupportedDatbaseDriverName(Exception): pass # noqa


def get_database(config):
    driver_name = config.get_database_driver_name()

    if driver_name == 'sql':
        engine = create_async_engine(config.get_sql_database_connection_url())

        return SQLDatabase(engine)
    else:
        raise UnsupportedDatbaseDriverName(driver_name)
