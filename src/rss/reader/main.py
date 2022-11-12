import logging

from logging.config import fileConfig

from dotenv import load_dotenv

load_dotenv('.env')
fileConfig('logging.ini')


from fastapi import FastAPI

from rss.reader.middlewares import config_middlewares
from rss.reader.openapi import config_openapi
from rss.reader.routes import config_routes


logger = logging.getLogger(__name__)


def main():
    app = FastAPI(debug=(logger.level == logging.DEBUG))

    config_middlewares(app)
    config_routes(app)
    config_openapi(app)

    logger.info('Server up')
    return app


if __name__ == '__main__':
    main()
