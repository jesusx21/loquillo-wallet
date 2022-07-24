from config import Config


class TestConfig(Config):
    def __init__(self, config_file_path):
        super().__init__(config_file_path)

        self.use_in_memory_database()

    def use_sql_database(self):
        self.database_driver = 'sql'

    def use_in_memory_database(self):
        self.database_driver = 'memory'

    def get_database_driver_name(self):
        return self.database_driver

    def get_database_name(self):
        return self.get('database', 'test_database', fallback='mister_krabz_test')
