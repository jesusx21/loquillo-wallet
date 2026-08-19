import os
from configparser import ConfigParser


class Config(ConfigParser):
    def __init__(self, config_file: str = 'config.ini'):
        normalized_env = {}

        for key, value in os.environ.items():
            normalized_env[key.lower()] = value

        super().__init__(normalized_env)

        self._config_file_path = config_file

        self.read(config_file)
        self._database_adapter = 'asyncpg'

    @property
    def database_driver(self) -> str:
        return self.get('database', 'driver')

    @property
    def database_name(self) -> str:
        return self.get('database', 'database')

    @property
    def sql_connection_uri(self) -> str:
        host = self.get('database', 'host', fallback='localhost')
        port = self.getint('database', 'port', fallback=5432)
        username = self.get('database', 'username')
        password = self.get('database', 'password', fallback=None)

        postgres_uri = f'postgresql+{self._database_adapter}://{username}'

        if password:
            postgres_uri += f':{password}'

        return f'{postgres_uri}@{host}:{port}/{self.database_name}'

    def with_database_adapter(self, adapter: str):
        self._database_adapter = adapter

        return self

    def _reset_database_adapter(self):
        self._database_adapter = 'asyncpg'
