from pydantic import BaseModel

class NotFound(BaseModel):
    detail: str
