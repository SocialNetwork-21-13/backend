from datetime import date, datetime
import datetime
from pydantic import BaseModel, EmailStr, validator, constr, Field
import uuid
from dotenv import dotenv_values
# from bson.objectid import ObjectId

config = dotenv_values(".env")

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    profile_image: str = str(config["DEFAULT_IMAGE_ID"])
    name: str
    surname : str
    email: EmailStr
    hashed_password: str
    username: str
    gender: str
    age: date
    created_at: datetime.datetime
    updated_at: datetime.datetime

class UserIn(BaseModel):
    name: str
    surname : str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    username : str
    gender : str
    age : date

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("passwords don't match")
        return v