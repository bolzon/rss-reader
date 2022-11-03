import logging

from functools import partial
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


logger = logging.getLogger(__name__)


def custom_openapi(app: FastAPI) -> dict[str, Any]:
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
        logger.info('Open API docs created')

    return app.openapi_schema


def config_openapi(app: FastAPI):
    app.openapi = partial(custom_openapi, app)