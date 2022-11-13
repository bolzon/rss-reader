# pylint: disable=wrong-import-order
import logging

from logging.config import fileConfig

from dotenv import load_dotenv


load_dotenv('.env')
fileConfig('logging.ini')


from typing import Any, Union

import dramatiq

from dramatiq.brokers.redis import RedisBroker

from rss.reader.email.sender import notify_user_feed_update_failed
from rss.reader.helpers import feeds as feeds_helper
from rss.reader.db.repository import RepositoryFactory


# number of feeds to read from DB for each batch update interaction
MAX_FEEDS_PER_READ = 500

logger = logging.getLogger(__name__)
redis_broker = RedisBroker(namespace='rss_reader')
dramatiq.set_broker(redis_broker)


@dramatiq.actor(actor_name='feed_update_failed')
def feed_update_failed(message: dict[str, Any], result: dict[str, Any]): # pylint: disable=unused-argument
    if not (feed_id := message.get('args', [None])[1]):
        return
    if not message.get('options', {}).get('retries', 0) >= 3:
        return
    repo = RepositoryFactory.create()
    db_feed = repo.feed.get_by_id(feed_id)
    db_user = repo.user.get_by_id(db_feed['user_id'])
    notify_user_feed_update_failed(user=db_user, feed=db_feed)


@dramatiq.actor(max_retries=2, on_failure='feed_update_failed',
                min_backoff=10*1000, max_backoff=30*1000)
def worker_update_feed(feed_id: Union[str, None] = None):
    if not feed_id:
        return
    logger.info('Updating feed %s', feed_id)
    repo = RepositoryFactory.create()
    feeds = repo.feed.get_by_ids([feed_id])
    if not feeds:
        logger.debug('Feed %s not found, exiting', feed_id)
        return
    feeds_helper.update_feed(feed_id=feed_id,
                             feed_dict=feeds[feed_id],
                             repo=repo)


@dramatiq.actor
def worker_update_feeds():
    logger.info('Updating feeds')
    repo = RepositoryFactory.create()
    # this reads limit number of feeds from DB
    # for each interaction using generator
    for feeds in repo.feed.get_all_simplified_gen(limit=MAX_FEEDS_PER_READ,
                                                  projection={'_id': 1}):
        for feed_id in feeds.keys():
            logger.debug('Enqueue update of feed %s', feed_id)
            worker_update_feed.send(feed_id)
