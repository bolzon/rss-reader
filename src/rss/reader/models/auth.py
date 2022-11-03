from pydantic import BaseModel


class AuthUser(BaseModel):
    id: str
    name: str


class AuthToken(BaseModel):
    access_token: str
    token_type: str


class Unauthorized(BaseModel):
    detail: str