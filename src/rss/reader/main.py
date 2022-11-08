import logging

from logging.config import fileConfig

from dotenv import load_dotenv

load_dotenv('.env')
fileConfig('logging.ini')


from fastapi import FastAPI

from rss.reader.middlewares import config_middlewares
from rss.reader.openapi import config_openapi
from rss.reader.routes import config_routes
from rss.reader.startup import config_startup


logger = logging.getLogger(__name__)

app = FastAPI(debug=(logger.level == logging.DEBUG))

config_startup(app)
config_middlewares(app)
config_routes(app)
config_openapi(app)

logger.info('Server up')
