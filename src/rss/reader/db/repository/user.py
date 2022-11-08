from typing import Any, Union

from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db_provider: DbProvider):
        super().__init__(db_provider, 'users')

    def create(self, user: dict[str, Any]) -> dict[str, Any]:
        return super().create(user)

    def get(self, filter: dict[str, Any],
            return_password: bool = False) -> Union[dict[str, Any], None]:
        args = {}
        if not return_password:
            args |= {'projection': {'password': False}}
        return super().get(filter=filter, **args)

    def get_all(self, filter: dict[str, Any] = {}, limit: int = 20,
                return_password: bool = False) -> list[dict[str, Any]]:
        args = {'limit': limit}
        if not return_password:
            args |= {'projection': {'password': False}}
        return list(super().get_all(filter=filter, **args))
