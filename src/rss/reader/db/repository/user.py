from typing import Any, Union

from pymongo.collection import Collection
from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db_provider: DbProvider):
        super().__init__(db_provider)
        self.users: Collection = db_provider.db['users']

    def create(self, user: dict[str, Any]) -> dict[str, Any]:
        res = self.users.insert_one(user)
        new_user = self.get(filter={'_id': res.inserted_id})
        return new_user

    def get(self, filter: dict[str, Any],
            return_password: bool = False) -> Union[dict[str, Any], None]:
        args = {'filter': filter}
        if not return_password:
            args.update({'projection': {'password': False}})
        return self.users.find_one(**args)

    def get_all(self, filter: dict[str, Any] = {}, limit: int = 20,
                return_password: bool = False) -> list[dict[str, Any]]:
        args = {'filter': filter, 'limit': limit}
        if not return_password:
            args.update({'projection': {'password': False}})
        return list(self.users.find(**args))
