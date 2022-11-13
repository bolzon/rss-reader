import logging
import os

from fastapi.encoders import jsonable_encoder

from rss.reader.db.repository import Repository, RepositoryFactory
from rss.reader.helpers import rss
from rss.reader.helpers.commons import exclude_none_keys


NUM_OF_WORKERS = os.cpu_count()

logger = logging.getLogger(__name__)


def update_feed(feed_id: str, feed_dict: dict[str, str],
                repo: Repository = RepositoryFactory.create()):
    '''Updated feed and its items in the database.

    Params:
        feed_id - feed ID
        feed_dict - feed dict {'user_id', 'url'}
        repo - database repository
    '''
    rss_data = rss.get_json_feed_from_url(feed_dict['url'])
    if not rss_data:
        raise RuntimeError(f'Invalid feed URL: {feed_dict["url"]} ({feed_id})')

    feed_dict |= rss.load_feed(rss_data=rss_data)
    item_list = rss.load_items(rss_data=rss_data, feed_id=feed_id,
                               user_id=feed_dict['user_id'])
    feed_dict = exclude_none_keys(feed_dict)
    repo.feed.update_by_id(feed_id, document=feed_dict)
    # switch by update_many with upsert option
    repo.item.create_many(jsonable_encoder(item_list.items))
