from pydantic import BaseModel, HttpUrl


class FollowRssFeed(BaseModel):
    url: HttpUrl


class UnfollowRssFeed(BaseModel):
    url: HttpUrl


class ListRssItems(BaseModel):
    id: str

class ForceUpdateRssFeed(BaseModel):
    id: str
