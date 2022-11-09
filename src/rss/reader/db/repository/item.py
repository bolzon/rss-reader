import logging

from typing import Any, Optional, Tuple, Union

from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.base import BaseRepository


logger = logging.getLogger(__name__)


class ItemRepository(BaseRepository):
    def __init__(self, db_provider: DbProvider):
        super().__init__(db_provider, 'items')

    def create(self, item: dict[str, Any]) -> dict[str, Any]:
        return super().create(item)

    def get_all_by_user_feed(self, user_id: str, feed_id: str,
                             limit: int = 20, **kwargs) -> list[dict[str, Any], None]:
        return self.get_all(filter={'user_id': user_id, 'feed_id': feed_id}, limit=limit, **kwargs)

    def get_all_by_user(self, user_id: str, limit: int = 20, **kwargs) -> list[dict[str, Any]]:
        return self.get_all(filter={'user_id': user_id}, limit=limit, **kwargs)

    def get_all_sorted(self, filter: dict[str, Any], limit: int = 20,
                       sorting: list[Tuple[str, int]] = [('pub_date', -1)],
                       **kwargs) -> list[dict[str, Any]]:
        args = {'filter': filter, 'limit': limit} | kwargs
        return list(self.col.find(**args).sort(sorting))

    def update_read_status(self, item_id: str, is_read: bool) -> Union[dict[str, Any], None]:
        return self.update(filter={'_id': item_id}, document={'is_read': is_read})
