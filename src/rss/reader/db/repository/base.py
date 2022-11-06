from rss.reader.db.provider import DbProvider


class BaseRepository:
    def __init__(self, db_provider: DbProvider):
        self.db_provider = db_provider
