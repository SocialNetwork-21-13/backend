from datetime import datetime, date
import datetime
from typing import List, Optional
from models.user import User, UserIn
from core.security import hash_password
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

def get_all(database, limit: int = 100, skip: int = 0) -> List[UserIn]:
    query = database["users"].find(limit=limit)
    return list(query)

def get_by_id(database, id : int) -> Optional[UserIn]:
    if (user := database["users"].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

def create(database, u : UserIn) -> User:
    user = User (
        name=u.name,
        email=u.email,
        hashed_password=hash_password(u.password),
        username=u.username,
        gender=u.gender,
        age=u.age,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    user = jsonable_encoder(user)
    new_user = database["users"].insert_one(user)
    created_user = database["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return new_user

def get_by_email(database, email: str) -> User:
    if (user := database["users"].find_one({"email": email})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found")