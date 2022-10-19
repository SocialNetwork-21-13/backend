from typing import List, Optional
import datetime as dt
from datetime import datetime
from models.post import Post, PostIn
from .base import BaseRepository
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
import gridfs
from bson import ObjectId
from repositories.user import UserRepository

users = UserRepository()

class PostRepository(BaseRepository):

    def create(self, user_id:str, file_id:str, p: PostIn) ->Post:
        post = Post(
            description=p.description,
            tags=p.tags,
            image=file_id,
            user_id=user_id,
            likes=0,
            created_at=dt.datetime.utcnow(),
            updated_at=dt.datetime.utcnow(),
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

    def sort_by_time(self,posts:list):
        posts=sorted(
            posts,
            key=lambda x: datetime.strptime(x['updated_at'], "%Y-%m-%dT%H:%M:%S.%f"), reverse=True
        )
        return posts

    def get_feed(self, user_id:str)-> List[Post]:
        feed=[]
        user=self.database["users"].find_one({"_id":user_id})
        subs=user["subscriptions"]
        for sub_user in subs:
            query = self.get_all_by_id(sub_user)
            feed=feed+query

        return self.sort_by_time(feed)

    def get_all_by_id(self,user_id:str) -> List[Post]:
        query = self.database["posts"].find({"user_id": user_id})
        return list(query)

    def get_by_id(self, id : int) -> Optional[Post]:
        if (post := self.database["posts"].find_one({"_id": id})) is not None:
            return post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")

    def delete(self, id: str,user_id:str):
        x=self.database["posts"].find_one({"_id": id})
        if x["user_id"]!=user_id:
            raise  HTTPException(status_code=403, detail='No access to delete this post')
        else:
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
        return self.database["posts"].find_one_and_update({'user_id': user_id},
                                                          {'$set': {"image": file_id}},
                                                          )
    
    def set_like(self, post_id : str, user_id : str) -> Post:
        self.database["users"].find_one_and_update({'_id': user_id},
                                                    {'$push': {"liked_posts": post_id}},
                                                )
        return self.database["posts"].find_one_and_update({'_id': post_id},
                                                          {'$inc': {"likes": 1}},
                                                          )

    def unset_like(self, post_id : str, user_id : str) -> Post:
        self.database["users"].find_one_and_update({'_id': user_id},
                                                    {'$pull': {"liked_posts": post_id}},
                                                )
        return self.database["posts"].find_one_and_update({'_id': post_id},
                                                          {'$inc': {"likes": -1}},
                                                          )



