import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
import uuid


class BasePost(BaseModel):
    #user_id: str
    description: str
    tags: list
    image : bytes

class Post(BasePost):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    created_at: datetime.datetime
    updated_at: datetime.datetime

class PostIn(BasePost):
    pass