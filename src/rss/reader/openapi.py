import logging

from functools import partial
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


logger = logging.getLogger(__name__)


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title='RSS Reader',
            version='1.0.0',
            description='RSS reader',
            routes=app.routes
        )
        logger.info('Open API docs created')

    return app.openapi_schema


def config_openapi(app: FastAPI):
    app.openapi = partial(custom_openapi, app)
