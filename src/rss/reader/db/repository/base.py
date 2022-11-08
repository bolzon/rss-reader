import logging

from typing import Any, Union

from rss.reader.db.provider import DbProvider


logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self, db_provider: DbProvider, collection_name: str):
        self.db_provider = db_provider
        self.col = self.db_provider.get_collection(collection_name)

    def create(self, document: dict[str, Any]) -> dict[str, Any]:
        res = self.col.insert_one(document)
        return self.get_by_id(res.inserted_id)

    def get(self, filter: dict[str, Any], **kwargs) -> Union[dict[str, Any], None]:
        args = {'filter': filter} | kwargs
        return self.col.find_one(**args)

    def get_by_id(self, id: str) -> Union[dict[str, Any], None]:
        return self.get(filter={'_id': id})

    def get_all(self, filter: dict[str, Any] = {}, limit: int = 20,
                **kwargs) -> list[dict[str, Any]]:
        args = {'filter': filter, 'limit': limit} | kwargs
        return list(self.col.find(**args))

    def update(self, filter: dict[str, Any],
               document: dict[str, Any]) -> dict[str, Any]:
        self.col.update_one(filter=filter, update=document, upsert=False)
        return self.get(filter=filter)
