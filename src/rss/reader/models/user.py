from pydantic import BaseModel, EmailStr


class SignupUser(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserAlreadyExists(BaseModel):
    detail: str
