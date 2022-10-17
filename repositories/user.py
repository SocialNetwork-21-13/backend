from datetime import datetime
import datetime
from typing import List, Optional

from fastapi import Body, Depends, FastAPI, APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.auth import Auth
from bson import ObjectId
from models.user import User, UserIn, AuthModel
from core.security import hash_password
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
import gridfs
from .base import BaseRepository
import os
# from core.config import DEFAULT_IMAGE_ID

security = HTTPBearer()
auth_handler = Auth()

DEFAULT_IMAGE_ID = ""

class UserRepository(BaseRepository):

    # User's profile methods

    def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = self.database["users"].find(limit=limit)
        return list(query)

    def get_by_id(self, id : int) -> Optional[User]:
        if (user := self.database["users"].find_one({"_id": id})) is not None:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

    def create(self, u : dict) -> User:
        user = User (
            username=u["username"],
            hashed_password=u["hashed_password"],
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        user.profile_image = os.getenv("DEFAULT_IMAGE_ID")
        user = jsonable_encoder(user)
        new_user = self.database["users"].insert_one(user)
        created_user = self.database["users"].find_one(
            {"_id": new_user.inserted_id}
        )
        return created_user

    def update(self, user_id : str, u : UserIn) -> User:
        return self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { 
                                "name" : u.name,
                                "surname" : u.surname,
                                "bio" : u.bio,
                                "age" : str(u.age),
                                "gender" : u.gender,
                                "email" : u.email,
                            } },
                            )

    def upload_image(self, file : bytes):
        imgs_profile = gridfs.GridFS(self.database, "imgs_profile")
        obj = imgs_profile.put(file)
        os.environ["DEFAULT_IMAGE_ID"] = str(imgs_profile.get(obj)._id)

    def get_by_email(self, email: str) -> User:
        if (user := self.database["users"].find_one({"email": email})) is not None:
            return user
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} not found")

    def get_file_id(self, file : bytes) -> str:
        imgs_profile = gridfs.GridFS(self.database, "imgs_profile")
        obj = imgs_profile.put(file)
        return str(imgs_profile.get(obj)._id)

    def update_name_surname(self, user_id : str, new_name : str, new_surname : str) -> User:
        return self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { 
                                "name" : new_name,
                                "surname" : new_surname,
                            } },
                            )

    def update_profile_image(self, user_id : str, file_id : str) -> User:
        user = self.database["users"].find_one({"_id" : user_id})
        if user["profile_image"] != os.getenv("DEFAULT_IMAGE_ID"):
            imgs_profile = gridfs.GridFS(self.database, "imgs_profile")
            imgs_profile.delete(ObjectId(user["profile_image"]))
        return self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { "profile_image" : file_id} },
                            )

    def update_username(self, user_id : str, new_username : str) -> User:
        return self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { "username" : new_username} },
                            )

    def delete(self, user_id : str):
        self.database["users"].find_one_and_delete({"_id" : user_id})

    def get_file(self, user_id : str) -> bytes:
        user = self.database["users"].find_one({"_id" : user_id})
        imgs_profile = gridfs.GridFS(self.database, "imgs_profile")
        file = imgs_profile.get(ObjectId(user["profile_image"]))
        return file.read()

    def update_bio(self, user_id : str, new_bio : str) -> User:
        return self.database["users"].find_one_and_update({'_id': user_id},
                            { '$set': { "bio" : new_bio} },
                            )
        
    def subscribe(self, user_id : str, sub_user_id : str):
        self.database["users"].find_one_and_update({'_id': user_id},
                            { '$push': { "subscriptions" : sub_user_id} },
                            )   
        self.database["users"].find_one_and_update({'_id': sub_user_id},
                            { '$push': { "subscribers" : user_id} },
                            )   
    
    def unsubsribe(self, user_id : str, sub_user_id : str):
        self.database["users"].find_one_and_update({'_id': user_id},
                            { '$pull': { "subscriptions" : sub_user_id} },
                            )
        self.database["users"].find_one_and_update({'_id': sub_user_id},
                            { '$pull': { "subscribers" : user_id} },
                            )
    
    def get_sub_helper(self, user_id : str, what_need : str) -> List[User]:
        user = self.database["users"].find_one({"_id" : user_id})
        res = []
        for u_id in user[what_need]:
            u = self.database["users"].find_one({"_id" : u_id})
            res.append(u)
        return res

    def get_subscribers(self, user_id : str) -> List[User]:
        return self.get_sub_helper(user_id, "subscribers")
        
    def get_subscriptions(self, user_id : str) -> List[User]:
        return self.get_sub_helper(user_id, "subscriptions")

    def check_username(self, username : str) -> bool:
        if self.database["users"].find_one({"username" : username}) is None:
            return False
        return True

    def get_by_username(self, username : str) -> Optional[User]:
        return self.database["users"].find_one({"username" : username})
    
    # User' login methods

    def signup(self, username : str, password : str) -> User:
        if self.check_username(username):
            return HTTPException(status_code=401, detail='Account already exists')
        try:
            hashed_password = auth_handler.encode_password(password)
            user = {"username": username, 'hashed_password': hashed_password}
            return self.create(user)
        except:
            return HTTPException(status_code=401, detail='Failed to signup user')

    def login(self, username : str, password : str) -> User:
        user = self.get_by_username(username)
        if self.check_username(username) is False:
            return HTTPException(status_code=401, detail='Invalid username')
        if (not auth_handler.verify_password(password, user['hashed_password'])):
            return HTTPException(status_code=401, detail='Invalid password')
        return user

    def get_current_user(self,token : str) -> User:
        username = auth_handler.decode_token(token)
        return self.get_by_username(username)