from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware


def config_middlewares(app: FastAPI):
    app.add_middleware(GZipMiddleware, minimum_size=1000)
