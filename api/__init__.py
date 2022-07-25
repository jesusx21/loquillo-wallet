from api.v1.wallets import WalletsResource


class MisterKrabzApp:
    def __init__(self, app):
        self._app = app

    def install(self):
        database = self._app.get_database()

        wallet_resource = WalletsResource(database)

        self._app.register_resource('wallets', wallet_resource)
