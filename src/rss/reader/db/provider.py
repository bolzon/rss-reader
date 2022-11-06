import logging

from pymongo import MongoClient


logger = logging.getLogger(__name__)


class DbProvider:
    def __init__(self, url: str, dbname: str):
        self.client = MongoClient(url)
        self.db = self.client[dbname]
        logger.info('Connected to DB: %s (%s)', url, dbname)

    def close(self):
        logger.info('Closing DB connection')
        self.db.close()
