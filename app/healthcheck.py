from falcon import HTTP_OK


class HealthCheck:
    async def on_get(self, req, resp):
        resp.status = HTTP_OK
        resp.media = {'status': 'ok'}
