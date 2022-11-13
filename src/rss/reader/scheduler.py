import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler

from rss.reader.workers.feeds import worker_update_feeds


FEEDS_UPDATE_INTERVAL = int(os.getenv('FEEDS_UPDATE_INTERVAL', '15'))

logger = logging.getLogger(__name__)


def create() -> BackgroundScheduler:
    scheduler = BackgroundScheduler({
        'apscheduler.jobstores.mongo': {
            'type': 'mongodb'
        }
    })

    scheduler.add_job(worker_update_feeds.send, 'interval',
                      minutes=FEEDS_UPDATE_INTERVAL)

    logger.info('Created background scheduler to update feeds each %d minute(s)',
                FEEDS_UPDATE_INTERVAL)

    return scheduler
