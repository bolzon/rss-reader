import logging

from fastapi import APIRouter, Request

from rss.reader.domain.rss_feed import RssFeedList
from rss.reader.domain.rss_item import RssItemList


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/{feed_id}/items', response_model=RssFeedList)
def find_items(feed_id: str, request: Request):
    return RssItemList(items=list(
        request.app.col_rss_items.find(
            filter={'user_id': request.user.id, 'feed_id': feed_id},
            limit=20
        )
    ))


@router.get('/', response_model=RssFeedList)
def find_feeds(request: Request):
    return RssFeedList(feeds=list(
        request.app.col_rss_feeds.find(
            filter={'user_id': request.user.id},
            limit=20
        )
    ))
