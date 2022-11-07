from typing import Any, Union

from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.base import BaseRepository


class FeedRepository(BaseRepository):
    def __init__(self, db_provider: DbProvider):
        super().__init__(db_provider, 'feeds')

    def create(self, user_id: str, feed: dict[str, Any]) -> dict[str, Any]:
        feed['user_id'] = user_id
        return super().create(feed)

    def get_by_user(self, user_id: str) -> Union[dict[str, Any], None]:
        return self.get(filter={'user_id': user_id})

    def get_all_by_user(self, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
        return self.get_all(filter={'user_id': user_id}, limit=limit)
