import json

from falcon import HTTP_CREATED, HTTP_OK

from app.errors import HTTPBadRequest, HTTPInternalServerError


class WalletsResource:
    def __init__(self, wallets):
        self._wallets = wallets

    async def on_post(self, req, resp):
        data = await req.media

        if (not data['name']) or (data['name'] == ''):
            raise HTTPBadRequest('NAME_MISSING')

        try:
            wallet = await self._wallets.create(name=data['name'])
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_CREATED
        resp.media = self._format_wallet(wallet)

    async def on_get(self, _req, resp):
        try:
            wallets = await self._wallets.get_list()
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_OK
        resp.media = self._format_wallets(wallets)

    def _format_wallet(self, wallet):
        return({
            'id': wallet.id,
            'name': wallet.name,
            'createdAt': wallet.created_at,
            'updatedAt': wallet.updated_at
        })

    def _format_wallets(self, wallets):
        result = map(self._format_wallet, wallets)

        return list(result)
