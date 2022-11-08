import uuid

from typing import Optional

from pydantic import BaseModel, Field


class RssFeed(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    user_id: str
    url: str
    title: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None


class RssFeedList(BaseModel):
    feeds: list[RssFeed] = []
