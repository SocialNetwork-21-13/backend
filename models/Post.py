import datetime
from pydantic import BaseModel


class BasePost(BaseModel):

    description: str
    author: str
#   Подумать нужно ли в посте хранить image или оно в текст будет вписываться


class Post(BasePost):
    id: int
    user_id: int
    slug: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PostIn(BasePost):
    pass