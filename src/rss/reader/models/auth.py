from pydantic import BaseModel


class Login(BaseModel):
    email: str
    pwd: str


class AuthToken(BaseModel):
    token: str


class Unauthorized(BaseModel):
    detail: str