import os

from fastapi import FastAPI

from rss.reader.db.repository import Repository


def config_startup(app: FastAPI):
    @app.on_event('startup')
    def startup():
        app.repository = Repository(
            os.environ['MONGO_URL'],
            os.environ['MONGO_DB_NAME']
        )

    @app.on_event('shutdown')
    def shutdown():
        app.repository.close()
