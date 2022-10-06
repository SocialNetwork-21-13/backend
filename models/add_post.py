import datetime
from pydantic import BaseModel


class BasePost(BaseModel):

    description: str
    author: str
#   Подумать нужно ли в посте image или оно в тексте будет каким-то образом

class Post(BasePost):
    id: int
    user_id: int
    slag: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PostIn(BasePost):
    pass