from typing import Any, Union

from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db_provider: DbProvider):
        super().__init__(db_provider, 'users')

    def get(self, query: dict[str, Any],
            return_password: bool = False) -> Union[dict[str, Any], None]:
        args = {}
        if not return_password:
            args |= {'projection': {'password': 0}}
        return super().get(query=query, **args)

    def get_by_id(self, id: str, return_password: bool = False) -> Union[dict[str, Any], None]:
        return self.get(query={'_id': id}, return_password=return_password)

    def get_all(self, query: Union[dict[str, Any], None] = None,
                limit: int = 20, return_password: bool = False) -> list[dict[str, Any]]:
        args = {'limit': limit}
        if not query:
            query = {}
        if not return_password:
            args |= {'projection': {'password': 0}}
        return list(super().get_all(query=query, **args))
