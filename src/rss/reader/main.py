import logging

from logging.config import fileConfig

from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pymongo import MongoClient


fileConfig('logging.ini')

logger = logging.getLogger(__name__)
config = dotenv_values('.env')

app = FastAPI()


@app.on_event('startup')
def startup():
    db_name = config['MONGO_DB_NAME']
    app.dbcli = MongoClient(config['MONGO_URL'])
    app.db = app.dbcli[db_name]


@app.on_event('shutdown')
def shutdown():
    app.dbcli.close()


@app.get('/')
def read_root():
    return {'hello': 'world'}


def config_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title='Sendcloud RSS Reader',
            version='1.0.0',
            description='RSS reader solution presented as part of the Sendcloud recruitment process.',
            routes=app.routes,
            contact={
                'name': 'Alexandre Bolzon',
                'email': 'hi@abolzon.com'
            }
        )
        app.openapi_schema['info']['x-logo'] = {
            'url': 'https://www.sendcloud.com/wp-content/uploads/2022/07/sendcloud-logo.png'
        }
    return app.openapi_schema


app.openapi = config_openapi