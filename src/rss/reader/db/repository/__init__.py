from rss.reader.db.provider import DbProvider
from rss.reader.db.repository.feed import FeedRepository
from rss.reader.db.repository.item import ItemRepository
from rss.reader.db.repository.user import UserRepository


class Repository:
    def __init__(self, mongo_url: str, mongo_dbname: str):
        self.db_provider = DbProvider(url=mongo_url, dbname=mongo_dbname)
        self.user = UserRepository(self.db_provider)
        self.feed = FeedRepository(self.db_provider)
        self.item = ItemRepository(self.db_provider)

    def close(self):
        self.db_provider.close()
