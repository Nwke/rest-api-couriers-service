from aiohttp.web_app import Application

from courier_service.api.handlers import HANDLERS

MEGABYTE = 1024 ** 2
MAX_REQUEST_SIZE = 70 * MEGABYTE


def create_app():
    app = Application(client_max_size=MAX_REQUEST_SIZE)

    for handler in HANDLERS:
        app.router.add_route('*', handler.URL_PATH, handler)

    return app
