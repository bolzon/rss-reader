import logging

from typing import Any, Union

from pymongo.results import UpdateResult

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

    def count(self, query: Union[dict[str, Any], None] = None, **kwargs) -> int:
        '''Count documents in collection.'''
        if not query:
            query = {}
        return self.col.count_documents(filter=query, **kwargs)

    def get(self, query: dict[str, Any], **kwargs) -> Union[dict[str, Any], None]:
        args = {'filter': query} | kwargs
        return self.col.find_one(**args)

    def get_by_id(self, id: str) -> Union[dict[str, Any], None]:
        return self.get(query={'_id': id})

    def get_all(self, query: Union[dict[str, Any], None] = None, limit: int = 20,
                **kwargs) -> list[dict[str, Any]]:
        if not query:
            query = {}
        args = {'filter': query, 'limit': limit} | kwargs
        return list(self.col.find(**args))

    def update_by_id(self, id: str, document: dict[str, Any]) -> UpdateResult:
        return self.update(query={'_id': id}, document=document)

    def update(self, query: dict[str, Any],
               document: dict[str, Any]) -> UpdateResult:
        if '_id' in document:
            del document['_id']
        return self.col.update_one(filter=query, update={'$set': document})

    def delete(self, query: dict[str, Any]) -> int:
        res = self.col.delete_one(filter=query)
        return res.deleted_count

    def delete_all(self, query: dict[str, Any]) -> int:
        res = self.col.delete_many(filter=query)
        return res.deleted_count
