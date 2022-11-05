"""Schemas"""
import pydantic
from datetime import datetime


class User(pydantic.BaseModel):
    name: str
    email: pydantic.EmailStr
    password: str

    class Config:
        orm_mode = True


class UserLogin(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str


class PostBase(pydantic.BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    published: bool = True
    owner_id: int
    owner: User

    class Config:
        orm_mode = True

class PostWithVote(pydantic.BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class CreatePost(PostBase):
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True


class UpdatePost(PostBase):
    title: str
    content: str

    class Config:
        orm_mode = True


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    id: int


class InvalidVoteDirection(Exception):
    """Custom error for invalid number in vote's direction"""

    def __init__(self, message):
        super().__init__(message)


class Vote(pydantic.BaseModel):
    post_id: int
    direction: int

    @pydantic.validator("direction")
    @classmethod
    def constraint(cls, value) -> None:
        """Constraint on value of direction"""
        if value not in [0, 1]:
            raise InvalidVoteDirection("Vote should be 0 or 1.")
        return value
