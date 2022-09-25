from uuid import UUID
from falcon import HTTP_CREATED, HTTP_OK

from app.errors import HTTPBadRequest, HTTPInternalServerError, HTTPNotFound
from mister_krabz.errors import ParentCategoryNotFound


class SubcategoriesResource:
    def __init__(self, categories):
        self._categories = categories

    async def on_post(self, req, resp, category_id):
        try:
            category_id = UUID(category_id)
        except ValueError as error:
            raise HTTPBadRequest('INVALID_ID', error)

        data = await req.media

        if (not data['name']) or (data['name'] == ''):
            raise HTTPBadRequest('NAME_MISSING')

        try:
            category = await self._categories.create(
                name=data['name'],
                parent_category_id=category_id
            )
        except ParentCategoryNotFound:
            raise HTTPNotFound('CATEGORY_NOT_FOUND')
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_CREATED
        resp.media = self.format_category(category)

    def format_category(self, category):
        return {
            'id': str(category.id),
            'name': category.name,
            'createdAt': category.created_at,
            'updatedAt': category.updated_at
        }

    def format_categories(self, categories):
        result = map(self.format_category, categories)

        return list(result)
