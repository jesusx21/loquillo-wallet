from api.v1.categories import CategoriesResource
from api.v1.category import CategoryResource
from api.v1.wallet import WalletResource
from api.v1.wallets import WalletsResource

from mister_krabz import Categories, Wallets


class MisterKrabzApp:
    def __init__(self, app):
        self._app = app

    def install(self):
        database = self._app.get_database()
        categories = Categories(database)
        wallets = Wallets(database)

        categories_resource = CategoriesResource(categories)
        category_resource = CategoryResource(categories)
        wallet_resource = WalletResource(wallets)
        wallets_resource = WalletsResource(wallets)

        self._app.register_resource('categories', categories_resource)
        self._app.register_resource('categories/{category_id}', category_resource)
        self._app.register_resource('wallets', wallets_resource)
        self._app.register_resource('wallets/{wallet_id}', wallet_resource)
