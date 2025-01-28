from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    fullname: str
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    fullname: str
    username: str
    email: EmailStr

