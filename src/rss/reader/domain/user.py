import uuid

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    name: str
    email: str
    password: str