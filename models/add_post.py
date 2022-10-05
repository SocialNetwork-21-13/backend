import datetime
from pydantic import BaseModel


class BaseJob(BaseModel):

    description: str
    author: str
#   Подумать нужно ли в посте image или оно в тексте будет каким-то образом

class Job(BaseJob):
    id: int
    user_id: int
    slag: str
    created_at: datetime.datetime
    updated_at: datetime.datetime


class JobIn(BaseJob):
    pass