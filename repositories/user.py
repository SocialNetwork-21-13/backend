from datetime import datetime
import datetime
from typing import List, Optional
from models.user import User, UserIn
from core.security import hash_password
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import gridfs

def get_all_users(database, limit: int = 100, skip: int = 0) -> List[User]:
    query = database["users"].find(limit=limit)
    return list(query)

def get_user_by_id(database, id : int) -> Optional[User]:
    if (user := database["users"].find_one({"_id": id})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

def create_user(database, u : UserIn) -> User:
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
    return created_user

def get_by_email(database, email: str) -> User:
    if (user := database["users"].find_one({"email": email})) is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found")

def get_file_id(database, file : bytes) -> str:
    imgs_profile = gridfs.GridFS(database, "imgs_profile")
    obj = imgs_profile.put(file)
    return str(imgs_profile.get(obj)._id)