from datetime import datetime
import datetime
from typing import List, Optional

from bson import ObjectId
from models.user import User, UserIn
from core.security import hash_password
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import gridfs
from dotenv import dotenv_values
from .base import BaseRepository

config = dotenv_values(".env")

class UserRepository(BaseRepository):
    def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = self.database["users"].find(limit=limit)
        return list(query)

    def get_by_id(self, id : int) -> Optional[User]:
        if (user := self.database["users"].find_one({"_id": id})) is not None:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

    def create(self, u : UserIn) -> User:
        user = User (
            name=u.name,
            surname=u.surname,
            email=u.email,
            hashed_password=hash_password(u.password),
            username=u.username,
            gender=u.gender,
            age=u.age,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        user = jsonable_encoder(user)
        new_user = self.database["users"].insert_one(user)
        created_user = self.database["users"].find_one(
            {"_id": new_user.inserted_id}
        )
        return created_user

    def get_by_email(self, email: str) -> User:
        if (user := self.database["users"].find_one({"email": email})) is not None:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found")

    def get_file_id(self, file : bytes) -> str:
        imgs_profile = gridfs.GridFS(self.database, "imgs_profile")
        obj = imgs_profile.put(file)
        return str(imgs_profile.get(obj)._id)

    def update_name_surname(self, user_id : str, new_name : str, new_surname : str) -> User:
        self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { "name" : new_name} },
                            )
        return self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { "surname" : new_surname} },
                            )

    def update_profile_image(self, user_id : str, file_id : str) -> User:
        user = self.database["users"].find_one({"_id" : user_id})
        if user["profile_image"] != str(config["DEFAULT_IMAGE_ID"]):
            imgs_profile = gridfs.GridFS(self.database, "imgs_profile")
            imgs_profile.delete(ObjectId(user["profile_image"]))
        return self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { "profile_image" : file_id} },
                            )

    def update_username(self, user_id : str, new_username : str) -> User:
        return self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { "username" : new_username} },
                            )