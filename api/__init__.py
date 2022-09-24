from api.v1.wallet import WalletResource
from api.v1.wallets import WalletsResource

from mister_krabz import Wallets


class MisterKrabzApp:
    def __init__(self, app):
        self._app = app

    def install(self):
        database = self._app.get_database()
        wallets = Wallets(database)

        wallet_resource = WalletResource(wallets)
        wallets_resource = WalletsResource(wallets)

        self._app.register_resource('wallets', wallets_resource)
        self._app.register_resource('wallets/{wallet_id}', wallet_resource)
