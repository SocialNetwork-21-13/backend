import datetime
from datetime import date
from typing import Optional
import uuid

import pydantic
from pydantic import BaseModel, constr, EmailStr, Field

# from bson.objectid import ObjectId


class User(BaseModel):
    _id: str = Field(default_factory=uuid.uuid4, alias="_id")
    profile_image: str = ""
    name: str = ""
    surname: str = ""
    bio: str = ""
    email: Optional[pydantic.EmailStr]
    hashed_password: str
    username: str
    gender: str = ""
    age: Optional[date]
    liked_posts: list = []
    subscriptions: list = []
    subscribers: list = []
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserIn(BaseModel):
    name: str
    surname: str
    bio: str
    email: EmailStr
    gender: str
    age: date


class AuthModel(BaseModel):
    username: str
    password: constr(min_length=8)
