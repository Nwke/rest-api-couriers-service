from http import HTTPStatus

from aiohttp.web import run_app

from courier_service.api.app import create_app


def main():
    app = create_app()

    run_app(app)


if __name__ == '__main__':
    main()
