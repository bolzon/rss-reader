from pydantic import BaseModel


class DeletedResponse(BaseModel):
    deleted: int
