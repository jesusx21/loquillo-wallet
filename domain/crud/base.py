from database.stores import Database


class CRUDBase:
    def __init__(self, database: Database):
        self._database = database
        self.__original_database = database

    def with_database(self, database: Database):
        self._database = database

        return self

    def restore_database(self):
        self._database = self.__original_database

        return self
