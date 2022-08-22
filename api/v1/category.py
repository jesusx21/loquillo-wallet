from uuid import UUID

from falcon import HTTP_OK

from app.errors import HTTPBadRequest, HTTPNotFound, HTTPInternalServerError
from mister_krabz.errors import CategoryNotFound


class CategoryResource:
    def __init__(self, categories):
        self._categories = categories

    async def on_get(self, _req, resp, category_id):
        try:
            category_id = UUID(category_id)
        except ValueError as error:
            raise HTTPBadRequest('INVALID_ID', error)

        try:
            category = await self._categories.get_by_id(category_id)
        except CategoryNotFound:
            raise HTTPNotFound('CATEGORY_NOT_FOUND')
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_OK
        resp.media = self.format_category(category)

    def format_category(self, category):
        return {
            'id': str(category['id']),
            'name': category['name'],
            'createdAt': category['created_at'],
            'updatedAt': category['updated_at']
        }
