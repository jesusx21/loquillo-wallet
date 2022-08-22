from humps import camelize

from falcon import HTTP_CREATED, HTTP_OK

from app.errors import HTTPBadRequest, HTTPInternalServerError


class CategoriesResource:
    def __init__(self, categories):
        self._categories = categories

    async def on_post(self, req, resp):
        data = await req.media

        if (not data['name']) or (data['name'] == ''):
            raise HTTPBadRequest('NAME_MISSING')

        try:
            category = await self._categories.create(name=data['name'])
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_CREATED
        resp.media = camelize(category)

    async def on_get(self, _req, resp):
        try:
            categories = await self._categories.get_list()
        except Exception as error:
            raise HTTPInternalServerError(cause=error)

        resp.status = HTTP_OK
        resp.media = camelize(categories)
