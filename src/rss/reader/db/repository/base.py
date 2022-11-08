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

    def create_many(self, documents: list[dict[str, Any]]) -> list[str]:
        res = self.col.insert_many(documents)
        return list(res.inserted_ids)

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
        if '_id' in document:
            del document['_id']
        self.col.update_one(filter=filter, update={'$set': document})
        return self.get(filter=filter)

    def delete(self, filter: dict[str, Any]) -> int:
        res = self.col.delete_one(filter=filter)
        return res.deleted_count

    def delete_all(self, filter: dict[str, Any]) -> int:
        res = self.col.delete_many(filter=filter)
        return res.deleted_count
