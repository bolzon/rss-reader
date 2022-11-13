import logging

from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Request, status
from rss.reader.db.repository import Repository

from rss.reader.domain.rss_item import RssItemList
from rss.reader.injections.repo import db_repo
from rss.reader.models.not_found import NotFound


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=RssItemList)
def list_items(request: Request, is_read: Union[bool, None] = None,
               repo: Repository = Depends(db_repo)):
    json_filter = {'user_id': request.user.id}
    if is_read is not None:
        json_filter |= {'is_read': is_read}
    return RssItemList(items=repo.item.get_all_sorted(query=json_filter))


@router.get('/feed/{feed_id}', response_model=RssItemList,
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def list_items_from_feed(request: Request, feed_id: str,
                         is_read: Union[bool, None] = None,
                         repo: Repository = Depends(db_repo)):
    db_feed = repo.feed.get_by_id(feed_id)
    if not db_feed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Feed with id "{feed_id}" not found')
    json_filter = {'user_id': request.user.id, 'feed_id': feed_id}
    if is_read is not None:
        json_filter |= {'is_read': is_read}
    return RssItemList(items=repo.item.get_all_sorted(query=json_filter))


@router.put('/{id}/read', responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def mark_as_read(id: str, repo: Repository = Depends(db_repo)):
    res = repo.item.update_by_id(id=id, document={'is_read': True})
    if res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Item with id "{id}" not found')


@router.put('/{id}/unread', responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def mark_as_unread(id: str, repo: Repository = Depends(db_repo)):
    res = repo.item.update_by_id(id=id, document={'is_read': False})
    if not res.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Item with id "{id}" not found')
