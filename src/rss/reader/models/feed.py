from pydantic import BaseModel


class FollowRssFeed(BaseModel):
    url: str


class UnfollowRssFeed(BaseModel):
    id: str


class ListRssItems(BaseModel):
    id: str
