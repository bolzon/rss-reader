import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from rss.reader.db.repository import Repository

from rss.reader.domain.rss_feed import RssFeed, RssFeedList
from rss.reader.injections.repo import db_repo
from rss.reader.models.deleted import DeletedResponse
from rss.reader.models.feed import FollowRssFeed, ForceUpdateRssFeed, UnfollowRssFeed
from rss.reader.models.not_found import NotFound
from rss.reader.workers.feeds import worker_update_feeds


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=RssFeedList)
def list_feeds(request: Request, repo: Repository = Depends(db_repo)):
    return RssFeedList(feeds=repo.feed.get_all_by_user(user_id=request.user.id))


@router.put('/', response_model=RssFeed,
            status_code=status.HTTP_202_ACCEPTED,
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def force_update(request: Request, feed: ForceUpdateRssFeed, repo: Repository = Depends(db_repo)):
    db_feed = repo.feed.get(query={'_id': feed.id,
                                   'user_id': request.user.id})
    if not db_feed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Feed with id "{id}" not found')
    worker_update_feeds.send([feed.id])
    return repo.feed.get_by_id(feed.id)


@router.post('/follow', response_model=RssFeed)
def follow(request: Request, feed: FollowRssFeed, repo: Repository = Depends(db_repo)):
    logger.debug('Checking existing feed: %s', feed.url)
    db_feed = repo.feed.get(query={'user_id': request.user.id,
                                   'url': feed.url.lower()})
    if not db_feed:
        logger.debug('No feed found, creating one')
        db_feed = repo.feed.create(jsonable_encoder(
            RssFeed(user_id=request.user.id,
                    url=feed.url.lower())
        ))
        logger.debug('Feed created: %s', db_feed)
        worker_update_feeds.send([db_feed['_id']])
    return db_feed


@router.post('/unfollow', response_model=DeletedResponse,
             responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def unfollow(request: Request, feed: UnfollowRssFeed, repo: Repository = Depends(db_repo)):
    db_feed = repo.feed.get(query={'user_id': request.user.id,
                                   'url': feed.url.lower()})
    if not db_feed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Feed with id "{id}" not found')
    feed_id = db_feed['_id']
    items_count = repo.item.delete_all(query={'user_id': request.user.id,
                                              'feed_id': feed_id})
    feed_count = repo.feed.delete(query={'_id': feed_id})
    return DeletedResponse(deleted=items_count + feed_count)
