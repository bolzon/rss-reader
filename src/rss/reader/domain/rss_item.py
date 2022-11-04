import uuid

from pydantic import BaseModel, Field


class RssItem(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    name: str
    title: str
    link: str
    description: str
    pub_date: str


class RssItemList(BaseModel):
    items: list[RssItem]
