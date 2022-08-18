from falcon import CORSMiddleware
from falcon.asgi import App
from falcon.http_error import HTTPError as FalconHTTPError

from app.healthcheck import HealthCheck
from app.errors import HTTPError
from app.media import json_handler, json_only_error_serializer
from database import get_database


class MrKrabz(App):
    def __init__(self, config):
        middleware = [CORSMiddleware(allow_origins='*', allow_credentials='*')]

        super().__init__(middleware=middleware)
        self._config = config
        self._database = get_database(self._config)

        self._install_json_media_handler()
        self._install_health_check()
        self._add_custom_error_handlers()

        self.set_error_serializer(json_only_error_serializer)

    def get_database(self):
        return self._database

    def _install_json_media_handler(self):
        extra_handlers = {
            'application/json': json_handler,
        }

        self.req_options.media_handlers.update(extra_handlers)
        self.resp_options.media_handlers.update(extra_handlers)

    def _install_health_check(self):
        self.add_route('/MrKrabz/api/v1/health', HealthCheck())

    def register_resource(self, path, handler):
        self.add_route(f'/MrKrabz/api/v1/{path}', handler)

    def _add_custom_error_handlers(self):
        self.add_error_handler(HTTPError, self._custom_http_error_handler)
        self.add_error_handler(FalconHTTPError, self._custom_falcon_http_error_handler)

    async def _custom_http_error_handler(self, req, resp, error, _params):
        self._compose_error_response(req, resp, error)

    async def _custom_falcon_http_error_handler(self, req, resp, error, _params):
        self._compose_error_response(req, resp, HTTPError.from_falcon_error(error))
