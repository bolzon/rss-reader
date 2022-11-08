import json
import logging

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder

from rss.reader.db.repository.feed import FeedRepository
from rss.reader.db.repository.item import ItemRepository
from rss.reader.domain.rss_feed import RssFeed, RssFeedList
from rss.reader.domain.rss_item import RssItemList
from rss.reader.models.deleted import DeletedResponse
from rss.reader.models.feed import FollowRssFeed, UnfollowRssFeed
from rss.reader.models.not_found import NotFound
from rss.reader.services.feed import execute_update_feed


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=RssFeedList)
def list_feeds(request: Request):
    feed_repo: FeedRepository = request.app.repository.feed
    return RssFeedList(feeds=feed_repo.get_all_by_user(user_id=request.user.id))


@router.post('/follow', status_code=status.HTTP_201_CREATED, response_model=RssFeed)
def follow(request: Request, feed: FollowRssFeed):
    feed_repo: FeedRepository = request.app.repository.feed
    logger.debug('Checking existing feed: %s', feed.url)
    db_feed = feed_repo.get(filter={'user_id': request.user.id,
                                    'url': feed.url})
    if not db_feed:
        logger.debug('No feed found, creating one')
        try:
            db_feed = feed_repo.create(jsonable_encoder(
                RssFeed(user_id=request.user.id, url=feed.url.lower())))
            logger.debug('Feed created: %s', db_feed)
            domain_feed = RssFeed(**db_feed)
            execute_update_feed(feed_id=domain_feed.id,
                                feed_url=domain_feed.url)
            db_feed = feed_repo.get_by_id(domain_feed.id)
        except Exception as e:
            logger.exception(e)
    return db_feed


@router.post('/unfollow', responses={
    status.HTTP_200_OK: {'model': DeletedResponse},
    status.HTTP_404_NOT_FOUND: {'model': NotFound}
})
def unfollow(request: Request, feed: UnfollowRssFeed):
    feed_repo: FeedRepository = request.app.repository.feed
    db_feed = feed_repo.get_by_id(feed.id)
    if not db_feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Feed with id "{id}" not found'
        )
    item_repo: ItemRepository = request.app.repository.item
    items_count = item_repo.delete_all(filter={'user_id': request.user.id,
                                               'feed_id': feed.id})
    feed_count = feed_repo.delete(filter={'_id': feed.id})
    return DeletedResponse(deleted=items_count + feed_count)


@router.get('/{feed_id}/items', response_model=RssItemList,
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def list_items(request: Request, feed_id: str):
    feed_repo: FeedRepository = request.app.repository.feed
    db_feed = feed_repo.get_by_id(feed_id)
    if not db_feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Feed with id "{id}" not found'
        )
    item_repo: ItemRepository = request.app.repository.item
    return RssItemList(items=item_repo.get_all_by_user_feed(
        user_id=request.user.id,
        feed_id=feed_id
    ))
