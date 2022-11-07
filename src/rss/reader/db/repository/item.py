from typing import Any, Union

from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.base import BaseRepository


class ItemRepository(BaseRepository):
    def __init__(self, db_provider: DbProvider):
        super().__init__(db_provider, 'items')

    def create(self, user_id: str, feed_id: str, item: dict[str, Any]) -> dict[str, Any]:
        item['user_id'] = user_id
        item['feed_id'] = feed_id
        return super().create(item)

    def get_all_by_user_feed(self, user_id: str, feed_id: str,
                             limit: int = 20) -> list[dict[str, Any], None]:
        return self.get_all(filter={'user_id': user_id, 'feed_id': feed_id}, limit=limit)

    def get_all_by_user(self, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
        return self.get_all(filter={'user_id': user_id}, limit=limit)

    def update_read_status(self, item_id: str, is_read: bool) -> Union[dict[str, Any], None]:
        return self.update(filter={'_id': item_id}, document={'is_read': is_read})
