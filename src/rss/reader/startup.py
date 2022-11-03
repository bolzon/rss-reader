import logging

from fastapi import FastAPI
from pymongo import MongoClient


logger = logging.getLogger(__name__)


def config_startup(app: FastAPI):

    @app.on_event('startup')
    def startup():
        app.dbcli = MongoClient(app.config['MONGO_URL'])
        app.db = app.dbcli[app.config['MONGO_DB_NAME']]

        app.col_users = app.db['users']
        app.col_rss_feeds = app.db['rss_feeds']
        app.col_rss_items = app.db['rss_items']

        logger.info('Connected to DB: %s (%s)',
                    app.config['MONGO_URL'], app.config['MONGO_DB_NAME'])

    @app.on_event('shutdown')
    def shutdown():
        app.dbcli.close()
