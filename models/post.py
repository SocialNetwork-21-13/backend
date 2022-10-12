import datetime
from bson import ObjectId
from pydantic import BaseModel


class BasePost(BaseModel):
    description: str
    tags: list
    image : bytes

class Post(BasePost):
    id: ObjectId
    user_id: ObjectId
    slag: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class PostIn(BasePost):
    pass