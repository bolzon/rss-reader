import asyncio
import logging
import os

from collections import OrderedDict
from typing import Any

import requests
import xmltodict

from fastapi.encoders import jsonable_encoder

from rss.reader.domain.rss_feed import RssFeed
from rss.reader.db.repository import Repository
from rss.reader.helpers import rss


logger = logging.getLogger(__name__)


def get_repository() -> Repository:
    return Repository(mongo_url=os.environ['MONGO_URL'],
                      mongo_dbname=os.environ['MONGO_DB_NAME'])


def get_feed_from_url(url: str) -> OrderedDict[str, Any]:
    res = requests.get(url, timeout=20)
    content_type = res.headers.get('content-type', '').lower()
    logger.debug('Content type: %s', content_type)
    if content_type.find('application/rss+xml') < 0:
        raise RuntimeError(f'Invalid content type: {content_type}')
    return xmltodict.parse(res.content)


async def update_feed_async(feed_id: str, feed_url: str):
    repo = get_repository()
    try:
        db_feed = repo.feed.get_by_id(feed_id)
        logger.debug('Getting feed from url: %s', feed_url)
        rss_data = get_feed_from_url(feed_url)
        feed = RssFeed(**db_feed)
        rss.update_feed(rss_data=rss_data, feed=feed)
        repo.feed.update(filter={'_id': feed.id},
                         document=jsonable_encoder(feed))
        item_list = rss.get_items(rss_data=rss_data,
                                  feed_id=feed.id,
                                  user_id=feed.user_id)
        repo.item.create_many(jsonable_encoder(item_list.items))
    except Exception as e:
        logger.error(e)
    finally:
        repo.close()


def execute_update_feed(feed_id: str, feed_url: str = None):
    # TODO supposed to use dramatiq
    logger.debug('Async updating feed: %s', feed_id)
    asyncio.run(update_feed_async(feed_id=feed_id, feed_url=feed_url))
