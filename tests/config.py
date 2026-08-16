from app.config import Config


class TestConfig(Config):
    def __init__(self):
        super().__init__('tests/config.ini')

        self.use_in_memory_database()

    def use_sql_database(self):
        self._database_driver = 'sql'

    def use_in_memory_database(self):
        self._database_driver = 'memory'

    @property
    def database_driver(self) -> str:
        return self._database_driver

    def get_database_name(self):
        return self.get('database', 'test_database', fallback='mister_krabz_test')
