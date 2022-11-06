from fastapi import FastAPI

from rss.reader.db.repository import Repository


def config_startup(app: FastAPI):
    @app.on_event('startup')
    def startup():
        app.repository = Repository(
            app.config['MONGO_URL'],
            app.config['MONGO_DB_NAME']
        )

    @app.on_event('shutdown')
    def shutdown():
        app.repository.close()
