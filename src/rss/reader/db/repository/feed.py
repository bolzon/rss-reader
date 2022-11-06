from typing import Any

from pymongo.collection import Collection

from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.base import BaseRepository


class FeedRepository(BaseRepository):
    def __init__(self, db_provider: DbProvider):
        super().__init__(db_provider)
        self.feeds: Collection = db_provider.db['feeds']

    def get_all(self, filter: dict[str, Any] = {},
                limit: int = 20) -> list[dict[str, Any]]:
        args = {'filter': filter, 'limit': limit}
        return list(self.feeds.find(**args))

    def get_by_user(self, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
        print('asdasd')
        return self.get_all(filter={'user_id': user_id}, limit=limit)
