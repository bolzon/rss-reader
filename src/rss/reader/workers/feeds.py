from logging.config import fileConfig

from dotenv import load_dotenv

load_dotenv('.env')
fileConfig('logging.ini')


import asyncio
import logging
import os

from time import monotonic
from typing import Any, Union

import dramatiq

from dramatiq.brokers.redis import RedisBroker
from fastapi.encoders import jsonable_encoder

from rss.reader.db.repository import Repository
from rss.reader.helpers import rss
from rss.reader.helpers.commons import exclude_none_keys


# when number of feeds is greater than this limit,
# update will happen in parts no greater than it
FEED_SPLIT_COUNT = 2

NUM_OF_WORKERS = os.cpu_count()


logger = logging.getLogger(__name__)
repository: Repository = None
redis_broker = RedisBroker(namespace='rss_reader')
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def worker_update_feeds(feed_ids: Union[list[str], None] = None):
    if feed_ids:
        asyncio.run(async_update_feeds(feed_ids))
    # else:
    #     repository = get_repository()
    #     num_of_chunks = 1
    #     feeds_count = repository.feed.count()
    #     if feeds_count > FEED_SPLIT_COUNT:
    #         num_of_chunks = feeds_count / FEED_SPLIT_COUNT


def get_repository() -> Repository:
    global repository
    if not repository:
        repository = Repository(mongo_url=os.environ['MONGO_URL'],
                                mongo_dbname=os.environ['MONGO_DB_NAME'])
    return repository


async def task_update_feeds(queue: asyncio.Queue):
    repository = get_repository()
    while True:
        idx, feed_id, feed_dict = await queue.get()
        logger.debug('[Worker %d] Getting feed from url: %s',
                     idx, feed_dict['url'])

        try:
            rss_data = rss.get_json_feed_from_url(feed_dict['url'])
            if not rss_data:
                logger.info('Invalid feed URL: %s (%s)',
                            feed_dict['url'], feed_id)
                queue.task_done()
                continue

            feed_dict |= rss.load_feed(rss_data=rss_data, feed=feed_dict)
            item_list = rss.load_items(rss_data=rss_data, feed_id=feed_id,
                                       user_id=feed_dict['user_id'])
            feed_dict = exclude_none_keys(feed_dict)
        except Exception as e:
            print(e)

        logger.debug('[Worker %d] Updating feed %s: %s',
                     idx, feed_id, feed_dict)
        repository.feed.update_by_id(feed_id, document=feed_dict)

        # switch by update_many with upsert option
        logger.debug('[Worker %d] Updating items of feed %s', idx, feed_id)
        repository.item.create_many(jsonable_encoder(item_list.items))
        queue.task_done()


async def async_update_feeds(feed_ids: list[str]):
    logger.info('Triggered update feeds for IDs: %s', feed_ids)

    repository = get_repository()
    feeds = repository.feed.get_by_ids(feed_ids)

    queue = asyncio.Queue()
    for idx, (feed_id, feed_dict) in enumerate(feeds.items()):
        # used tuple for easy access
        queue.put_nowait((idx + 1, feed_id, feed_dict))

    tasks = []
    num_of_feeds = len(feed_ids)
    num_of_tasks = min(NUM_OF_WORKERS, num_of_feeds)

    logger.info('Updating feeds in %d task(s)', num_of_tasks)

    for i in range(num_of_tasks):
        tasks.append(asyncio.create_task(task_update_feeds(queue)))

    start_time = monotonic()
    await queue.join()
    time_taken = monotonic() - start_time

    logger.info('Time taken updating %d feed(s): %ds',
                num_of_feeds, time_taken)

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
