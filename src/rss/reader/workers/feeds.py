import asyncio
import logging
import os

from collections import OrderedDict
from typing import Any

import dramatiq
import requests
import xmltodict

from dramatiq.brokers.redis import RedisBroker
from fastapi.encoders import jsonable_encoder

from rss.reader.domain.rss_feed import RssFeed
from rss.reader.db.repository import Repository
from rss.reader.helpers import rss


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


async def get_feed_from_url(url: str) -> OrderedDict[str, Any]:
    res = requests.get(url, timeout=20)
    content_type = res.headers.get('content-type', '').lower()
    logger.debug('Content type: %s', content_type)
    if content_type.find('application/rss+xml') < 0:
        raise RuntimeError(f'Invalid content type: {content_type}')
    return xmltodict.parse(res.content)


def update_feeds_db():
    '''Update a few (up to 1000) feeds in the database at a time.'''


def update_many(feed_ids: list[str]):
    '''Update many (more than 1000) feeds in the database in a concurrent way.'''


def exclude_none(feed: dict[str, Any]) -> dict[str, Any]:
    '''Returns dict whose values are not None.'''
    return {k: v for k, v in feed.items() if v is not None}


def split_list(the_list: list[Any], items: int = 1000):
    '''Yield successive n-sized chunks from lst.'''
    for i in range(0, len(the_list), items):
        yield the_list[i:i + items]


@dramatiq.actor
def update(feed_ids: list[str]):
    repository = get_repository()
    feeds = repository.feed.get_urls_by_ids(feed_ids)

    # queue = asyncio.Queue()
    # for feed in feeds:
    #     queue.put_nowait(feed)

    for feed_id, feed_url in feeds.items():
        try:
            logger.debug('Getting feed from url: %s', feed_url)
            rss_data = get_feed_from_url(feed_url)
            feed = RssFeed(id=feed_id)
            rss.load_feed(rss_data=rss_data, feed=feed)
            json_feed = exclude_none(jsonable_encoder(feed))
            item_list = rss.load_items(rss_data=rss_data,
                                       feed_id=feed.id,
                                       user_id=feed.user_id)
            repository.feed.update_by_id(feed.id, document=json_feed)
            # switch by update_many with upsert option
            repository.item.create_many(jsonable_encoder(item_list.items))
        except Exception as e:
            logger.error(e)
