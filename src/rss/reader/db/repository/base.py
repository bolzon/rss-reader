from typing import Any, Union

from rss.reader.db.provider import DbProvider


class BaseRepository:
    def __init__(self, db_provider: DbProvider, collection_name: str):
        self.db_provider = db_provider
        self.col = self.db_provider.get_collection(collection_name)

    def create(self, document: dict[str, Any]) -> dict[str, Any]:
        res = self.col.insert_one(document)
        return self.get(filter={'_id': res.inserted_id})

    def get(self, filter: dict[str, Any], **kwargs) -> Union[dict[str, Any], None]:
        return self.col.find_one({'filter': filter} | kwargs)

    def get_by_id(self, id: str) -> Union[dict[str, Any], None]:
        return self.get(filter={'_id': id})

    def get_all(self, filter: dict[str, Any] = {}, limit: int = 20,
                **kwargs) -> list[dict[str, Any]]:
        args = {'filter': filter, 'limit': limit}
        return list(self.col.find(args | kwargs))

    def update(self, filter: dict[str, Any],
               document: dict[str, Any]) -> dict[str, Any]:
        self.col.update_one(filter=filter, update=document, upsert=False)
        return self.get(filter=filter)
