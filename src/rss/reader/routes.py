from fastapi import FastAPI

from rss.reader.routers.feed import router as feed_router
from rss.reader.routers.user import router as user_router


def config_routes(app: FastAPI):
    app.include_router(feed_router, prefix='/feed')
    app.include_router(user_router, prefix='/user')
