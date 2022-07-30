import os

from configparser import ConfigParser


class Config(ConfigParser):
    def __init__(self, config_file_path):
        super().__init__(os.environ)

        self._config_file_path = config_file_path

        self.read(config_file_path)

    def get_database_driver_name(self):
        return self.get('database', 'driver')

    def get_sql_database_connection_url(self, driver='asyncpg'):
        host = self.get('database', 'host', fallback='localhost')
        port = self.getint('database', 'port', fallback=5432)
        username = self.get('database', 'username')
        password = self.get('database', 'password', fallback=None)
        database = self.get_database_name()

        if password:
            return 'postgresql+%s://%s:%s@%s:%s/%s' % (
                driver, username, password, host, port, database
            )

        return 'postgresql+%s://%s@%s:%s/%s' % (
            driver, username, host, port, database
        )

    def get_database_name(self):
        return self.get('database', 'database')
