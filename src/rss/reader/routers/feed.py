import logging

from fastapi import APIRouter, Request

from rss.reader.domain.rss_feed import RssFeedList


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=RssFeedList)
def find_feeds(request: Request):
    return RssFeedList(feeds=list(
        request.app.col_rss_feeds.find(
            limit=20
        )
    ))