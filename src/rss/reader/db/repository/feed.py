from typing import Any, Union

from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.base import BaseRepository


class FeedRepository(BaseRepository):
    def __init__(self, db_provider: DbProvider):
        super().__init__(db_provider, 'feeds')

    def create(self, feed: dict[str, Any]) -> dict[str, Any]:
        return super().create(feed)

    def get_by_ids(self, ids: list[str], limit: int = 1000) -> Union[dict[str, str], None]:
        '''Return only feed ids and their user ids/urls to improve performance.
            [{ '<feed_id>': {'user_id': '<user_id>', 'url': '<url>'} }, {...}]
        '''
        args = {'projection': {'_id': 1, 'user_id': 1, 'url': 1}}
        if feeds := self.get_all(filter={'_id': {'$in': ids}}, limit=limit, **args):
            return {f['_id']: {'user_id': f['user_id'], 'url': f['url']} for f in feeds}
        return None

    def get_by_user(self, user_id: str) -> Union[dict[str, Any], None]:
        return self.get(filter={'user_id': user_id})

    def get_all_by_user(self, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
        return self.get_all(filter={'user_id': user_id}, limit=limit)
