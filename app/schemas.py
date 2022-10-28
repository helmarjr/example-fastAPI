from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


# ====================== VOTE ======================
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


# ====================== USER ======================
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str



# ====================== TOKEN ======================
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None



# ====================== POST ======================
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
