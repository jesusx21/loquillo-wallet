from uuid import UUID

from falcon import HTTP_OK

from app.errors import HTTPBadRequest, HTTPNotFound, HTTPInternalServerError
from mister_krabz.errors import WalletNotFound


class WalletResource:
    def __init__(self, wallets):
        self._wallets = wallets

    async def on_put(self, req, resp, wallet_id):
        try:
            wallet_id = UUID(wallet_id)
        except ValueError as error:
            raise HTTPBadRequest('INVALID_ID', error)

        data = await req.media

        try:
            wallet = await self._wallets.update(wallet_id, data['name'])
        except WalletNotFound:
            raise HTTPNotFound('WALLET_NOT_FOUND')
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_OK
        resp.media = self.format_wallet(wallet)

    async def on_get(self, _req, resp, wallet_id):
        try:
            wallet_id = UUID(wallet_id)
        except ValueError as error:
            raise HTTPBadRequest('INVALID_ID', error)

        try:
            wallet = await self._wallets.get_by_id(wallet_id)
        except WalletNotFound:
            raise HTTPNotFound('WALLET_NOT_FOUND')
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_OK
        resp.media = self.format_wallet(wallet)

    def format_wallet(self, wallet):
        return {
            'id': str(wallet.id),
            'name': wallet.name,
            'createdAt': wallet.created_at,
            'updatedAt': wallet.updated_at
        }
