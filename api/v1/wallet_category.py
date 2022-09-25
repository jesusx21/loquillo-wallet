from uuid import UUID
from falcon import HTTP_CREATED

from app.errors import HTTPBadRequest, HTTPInternalServerError, HTTPNotFound
from mister_krabz.errors import CategoryNotFound, WalletNotFound


class WalletCategoryResource:
    def __init__(self, wallets):
        self._wallets = wallets

    async def on_post(self, _req, resp, wallet_id, category_id):
        try:
            category_id = UUID(category_id)
            wallet_id = UUID(wallet_id)
        except ValueError as error:
            raise HTTPBadRequest('INVALID_ID', error)

        try:
            wallet_category = await self._wallets.add_category(wallet_id, category_id)
        except WalletNotFound:
            raise HTTPNotFound('WALLET_NOT_FOUND')
        except CategoryNotFound:
            raise HTTPNotFound('CATEGORY_NOT_FOUND')
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_CREATED
        resp.media = self.format_wallet_category(wallet_category)

    def format_wallet_category(self, wallet_category):
        return {
            'id': str(wallet_category._wallet.id),
            'name': wallet_category._wallet.name,
            'category': {
                'id': wallet_category._category.id,
                'name': wallet_category._category.name
            },
            'createdAt': wallet_category._wallet.created_at,
            'updatedAt': wallet_category._wallet.updated_at
        }
