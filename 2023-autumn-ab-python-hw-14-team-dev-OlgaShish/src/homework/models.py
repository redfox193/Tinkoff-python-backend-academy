from typing import Optional
from pydantic import BaseModel
from src.homework.tps import Tags


class User(BaseModel):
    login: str
    password: str
    first_name: str
    second_name: str
    skils: list[str]
    company: Optional[str]


class UserInfo(BaseModel):
    login: str
    password: str
    token: str


class UserInfoAuth(BaseModel):
    login: str
    password: str


class CreateOrUpdatePost(BaseModel):
    post_id: Optional[int]
    name: str
    text: str
    tags: list[Tags]
    token: str
    new_likes: Optional[int]
    new_dislikes: Optional[int]
    new_comments: list[str]


class GetPosts(BaseModel):
    author_id: Optional[int]
    tags: list[Tags]
    name_search: Optional[str]
    pagination_current: int


class DeletePost(BaseModel):
    post_id: int
    token: str
