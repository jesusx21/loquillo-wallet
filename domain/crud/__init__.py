from .accounts import Accounts
from .categories import Categories
from .transactions import Transactions
from .wallets import Wallets
from database.stores import Database


class CRUD:
    def __init__(self, database: Database):
        self.accounts = Accounts(database)
        self.categories = Categories(database)
        self.transactions = Transactions(database)
        self.wallets = Wallets(database)

    def with_database(self, database: Database):
        self.accounts.with_database(database)
        self.categories.with_database(database)
        self.transactions.with_database(database)
        self.wallets.with_database(database)

        return self

    def restore_database(self):
        self.accounts.restore_database()
        self.categories.restore_database()
        self.transactions.restore_database()
        self.wallets.restore_database()

        return self
