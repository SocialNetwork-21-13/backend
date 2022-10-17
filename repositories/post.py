from typing import List, Optional
import datetime
from models.post import Post, PostIn
from .base import BaseRepository
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
import gridfs
from bson import ObjectId

class PostRepository(BaseRepository):


    def create(self,user_id:str,file_id:str, p: PostIn) ->Post:
        post = Post(
            description=p.description,
            tags=p.tags,
            image=file_id,
            user_id=user_id,
            likes=0,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        post = jsonable_encoder(post)
        new_post = self.database["posts"].insert_one(post)
        created_post = self.database["posts"].find_one(
            {"_id": new_post.inserted_id}
        )
        return created_post

    def get_all(self, limit: int = 100, skip: int = 0) -> List[Post]:
        query = self.database["posts"].find(limit=limit)
        return list(query)

    def get_by_id(self, id : int) -> Optional[Post]:
        if (post := self.database["posts"].find_one({"_id": id})) is not None:
            return post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")

    def delete(self, id: str):
        self.database["posts"].find_one_and_delete({"_id": id})

    def upload_image(self, file : bytes):
        imgs_post=gridfs.GridFS(self.database, "imgs_post")
        obj = imgs_post.put(file)

    def get_file_id(self, file:bytes) ->str:
        imgs_post = gridfs.GridFS(self.database, "imgs_post")
        obj = imgs_post.put(file)
        return str(imgs_post.get(obj)._id)

    def get_file(self, post_id : str) ->bytes:
        post = self.database["posts"].find_one({"_id" : post_id})
        imgs_post=gridfs.GridFS(self.database, "imgs_post")
        file = imgs_post.get(ObjectId(post["image"]))
        return file.read()

    def set_post_image(self, user_id: str, file_id: str)->Post:
        post = self.database["posts"].find_one({"user_id": user_id})
        imgs_post = gridfs.GridFS(self.database, "imgs_post")
        return self.database["posts"].find_one_and_update({'user_id': user_id},
                                                          {'$set': {"image": file_id}},
                                                          )