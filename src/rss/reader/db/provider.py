import logging

from typing import Union

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


logger = logging.getLogger(__name__)


class DbProvider:
    def __init__(self, url: str, dbname: str):
        self.client: MongoClient = MongoClient(url)
        self.db: Database = self.client.get_database(dbname)
        logger.info('Connected to DB: %s (%s)', url, dbname)

    def get_db(self, db_name: str) -> Database:
        return self.client.get_database(db_name)

    def get_collection(self, collection_name: str,
                       db_name: Union[str, None] = None) -> Collection:
        db = self.db if db_name is None else self.get_db(db_name)
        return db.get_collection(collection_name)

    def close(self):
        logger.info('Closing DB connection')
        self.client.close()
