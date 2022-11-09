import logging

from typing import Union

from fastapi import APIRouter, HTTPException, Request, status

from rss.reader.db.repository.feed import FeedRepository
from rss.reader.db.repository.item import ItemRepository
from rss.reader.domain.rss_item import RssItem, RssItemList
from rss.reader.models.not_found import NotFound


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/', response_model=RssItemList)
def list_items(request: Request, is_read: Union[bool, None] = None):
    item_repo: ItemRepository = request.app.repository.item
    json_filter = {'user_id': request.user.id}
    if is_read is not None:
        json_filter |= {'is_read': is_read}
    return RssItemList(items=item_repo.get_all_sorted(filter=json_filter))


@router.get('/feed/{feed_id}', response_model=RssItemList,
            responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def list_items_from_feed(request: Request, feed_id: str, is_read: Union[bool, None] = None):
    feed_repo: FeedRepository = request.app.repository.feed
    db_feed = feed_repo.get_by_id(feed_id)
    if not db_feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Feed with id "{feed_id}" not found'
        )
    item_repo: ItemRepository = request.app.repository.item
    json_filter = {'user_id': request.user.id, 'feed_id': feed_id}
    if is_read is not None:
        json_filter |= {'is_read': is_read}
    return RssItemList(items=item_repo.get_all_sorted(filter=json_filter))


@router.post('/{id}/read', responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def mark_as_read(request: Request, id: str):
    item_repo: ItemRepository = request.app.repository.item
    res = item_repo.update_by_id(id=id, document={'is_read': True})
    if res.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item with id "{id}" not found'
        )


@router.post('/{id}/unread', responses={status.HTTP_404_NOT_FOUND: {'model': NotFound}})
def mark_as_unread(request: Request, id: str):
    item_repo: ItemRepository = request.app.repository.item
    res = item_repo.update_by_id(id=id, document={'is_read': False})
    if not res.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item with id "{id}" not found'
        )
