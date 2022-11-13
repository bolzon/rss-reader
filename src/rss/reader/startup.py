import os
from fastapi import FastAPI

from rss.reader import scheduler as task_scheduler

FEEDS_UPDATE_INTERVAL = int(os.getenv('FEEDS_UPDATE_INTERVAL', 15))


def config_startup(app: FastAPI):
    scheduler = task_scheduler.create()
    app.add_event_handler('startup', scheduler.start)
    app.add_event_handler('shutdown', scheduler.shutdown)
