import logging
import os

import dramatiq

from dramatiq.brokers.redis import RedisBroker
from fastapi.encoders import jsonable_encoder

from rss.reader.db.repository import Repository
from rss.reader.helpers import rss
from rss.reader.helpers.commons import exclude_none_keys


NUM_OF_WORKERS = os.cpu_count()

logger = logging.getLogger(__name__)
repository: Repository = None
redis_broker = RedisBroker(namespace='rss_reader')
dramatiq.set_broker(redis_broker)


def get_repository() -> Repository:
    global repository
    if not repository:
        repository = Repository(mongo_url=os.environ['MONGO_URL'],
                                mongo_dbname=os.environ['MONGO_DB_NAME'])
    return repository


def update_feeds_db():
    '''Update a few (up to 1000) feeds in the database at a time.'''


def update_many(feed_ids: list[str]):
    '''Update many (more than 1000) feeds in the database in a concurrent way.'''


@dramatiq.actor
def update(feed_ids: list[str]):
    repository = get_repository()
    feeds = repository.feed.get_by_ids(feed_ids)

    # queue = asyncio.Queue()
    # for feed in feeds:
    #     queue.put_nowait(feed)

    for feed_id, feed_dict in feeds.items():
        logger.debug('Getting feed from url: %s', feed_dict['url'])
        rss_data = rss.get_json_feed_from_url(feed_dict['url'])
        feed_dict |= rss.load_feed(rss_data=rss_data, feed=feed_dict)
        item_list = rss.load_items(rss_data=rss_data, feed_id=feed_id,
                                   user_id=feed_dict['user_id'])
        feed_dict = exclude_none_keys(feed_dict)
        repository.feed.update_by_id(feed_id, document=feed_dict)
        # switch by update_many with upsert option
        repository.item.create_many(jsonable_encoder(item_list.items))
