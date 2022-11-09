from pydantic import BaseModel, HttpUrl


class FollowRssFeed(BaseModel):
    url: HttpUrl


class UnfollowRssFeed(BaseModel):
    id: str


class ListRssItems(BaseModel):
    id: str
