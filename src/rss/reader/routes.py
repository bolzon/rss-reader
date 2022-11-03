from fastapi import APIRouter, Depends, FastAPI

from rss.reader.auth.provider import auth_user
from rss.reader.routers.feed import router as feed_router
from rss.reader.routers.login import router as login_router
from rss.reader.routers.user import router as user_router


def config_public_routes(app: FastAPI):
    app.include_router(login_router, prefix='/login')


def config_private_routes(app: FastAPI):
    auth_router = APIRouter(dependencies=[Depends(auth_user)],
                            responses={})
    auth_router.include_router(feed_router, prefix='/feed')
    auth_router.include_router(user_router, prefix='/user')
    app.include_router(auth_router)


def config_routes(app: FastAPI):
    config_public_routes(app)
    config_private_routes(app)