from aiohttp.web import View


class BaseView(View):
    URL_PATH: str
