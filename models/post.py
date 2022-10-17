import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
import uuid


class BasePost(BaseModel):
    description: str
    tags: list

class Post(BasePost):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    created_at: datetime.datetime
    updated_at: datetime.datetime
    user_id: str
    image: str
    likes: int

class PostIn(BasePost):
    pass