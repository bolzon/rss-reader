import logging

from fastapi import APIRouter, Request
from rss.reader.db.repository.feed import FeedRepository

from rss.reader.domain.rss_feed import RssFeedList
from rss.reader.domain.rss_item import RssItemList


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/{feed_id}/items', response_model=RssFeedList)
def find_items(feed_id: str, request: Request):
    feed_repo: FeedRepository = request.app.repository.feed
    return RssItemList(items=feed_repo.get_items(filter={
        'feed_id': feed_id,
        'user_id': request.user.id
    }))


@router.get('/', response_model=RssFeedList)
def find_feeds(request: Request):
    feed_repo: FeedRepository = request.app.repository.feed
    return RssFeedList(feeds=feed_repo.get_all_by_user(user_id=request.user.id))
