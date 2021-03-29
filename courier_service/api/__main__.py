import aiohttp.web

from courier_service.api.app import create_app


def main():
    app = create_app()
    aiohttp.web.run_app(app, host='localhost', port=8080)


if __name__ == '__main__':
    main()
