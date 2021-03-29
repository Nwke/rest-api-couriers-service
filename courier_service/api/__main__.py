import aiohttp.web

from courier_service.api.app import create_app


def main():
    app = create_app()
    aiohttp.web.run_app(app, host='0.0.0.0', port=80)


if __name__ == '__main__':
    main()