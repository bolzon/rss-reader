from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


app = FastAPI()


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