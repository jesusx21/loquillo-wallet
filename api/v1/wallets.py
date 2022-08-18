from curses.ascii import HT
from humps import camelize

from falcon import HTTP_CREATED

from app.errors import HTTPBadRequest, HTTPInternalServerError
from mister_krabz.wallets import CreateWallet


class WalletsResource:
    def __init__(self, database):
        self._database = database

    async def on_post(self, req, resp):
        data = await req.media

        if (not data['name']) or (data['name'] == ''):
            raise HTTPBadRequest('NAME_MISSING')

        create_wallet = CreateWallet(self._database, name=data['name'])

        try:
            wallet = await create_wallet.run()
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_CREATED
        resp.media = camelize(wallet)
