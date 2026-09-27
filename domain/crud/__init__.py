from .accounts import Accounts
from database.stores import Database


class CRUD:
    def __init__(self, database: Database):
        self.accounts = Accounts(database=database)

    def with_database(self, database: Database):
        self.accounts.with_database(database)

        return self

    def restore_database(self):
        self.accounts.restore_database()

        return self
