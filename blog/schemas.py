from datetime import datetime
from typing import List, Union

from pydantic import BaseModel
from pydantic.schema import Optional


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True


class ShowUserBlogs(ShowUser):
    blogs: List[Blog]

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    comment: str

    class Config:
        orm_mode = True


class Comment(CommentBase):
    created_at: datetime
    commentator: ShowUser = None

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    creator: ShowUser = None
    comments: Optional[List[Comment]]

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
