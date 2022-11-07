import uuid

from pydantic import BaseModel, Field

from rss.reader.domain.rss_item import RssItem


class RssFeed(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    user_id: str
    name: str
    title: str
    link: str
    description: str


class RssFeedList(BaseModel):
    feeds: list[RssFeed]
