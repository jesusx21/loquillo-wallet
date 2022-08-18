from api import MisterKrabzApp
from app.app import MrKrabz


def create_app(config):
    app = MrKrabz(config)
    mister_krabz_api = MisterKrabzApp(app)

    mister_krabz_api.install()

    return app
