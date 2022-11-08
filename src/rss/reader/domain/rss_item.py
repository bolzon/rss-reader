import uuid

from typing import Optional

from pydantic import BaseModel, Field


class RssItem(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    user_id: str
    feed_id: str
    title: Optional[str] = None
    link: Optional[str] = None
    description: Optional[str] = None
    pub_date: Optional[str] = None
    is_read: bool = False


class RssItemList(BaseModel):
    items: list[RssItem] = []
