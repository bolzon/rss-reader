from dotenv import dotenv_values
from logging.config import fileConfig

fileConfig('logging.ini')

from fastapi import FastAPI

from rss.reader.openapi import config_openapi
from rss.reader.routes import config_routes
from rss.reader.startup import config_startup


app = FastAPI()
app.config = dotenv_values('.env')

config_startup(app)
config_routes(app)
config_openapi(app)