from fastapi import APIRouter, status,Response, File, UploadFile, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import List
from repositories.post import PostRepository
from models.post import Post, PostIn
from repositories.user import UserRepository

router = APIRouter()

posts = PostRepository()
users = UserRepository()
security = HTTPBearer()

@router.post("/", response_description="Create a new post", status_code=status.HTTP_201_CREATED,response_model=Post)
def create(credentials: HTTPAuthorizationCredentials = Security(security),file: UploadFile=File(),post:PostIn=Depends()):
    file_id=posts.get_file_id(file.file)
    user = users.get_current_user(credentials.credentials)
    return posts.create(user["_id"],file_id, post)

@router.get("/", response_description="List all posts", response_model=List[Post])
def list_posts(limit : int = 100, skip : int = 0):
    return posts.get_all(limit=limit, skip=skip)

@router.put("/post_image", response_description="Set a new post image")
def upload_file(credentials: HTTPAuthorizationCredentials = Security(security), file: bytes = File()):
    file_id = posts.get_file_id(file)
    user = users.get_current_user(credentials.credentials)
    return posts.set_post_image(user["_id"], file_id)

@router.get("/get_post_image", response_description="Get post image")
def get_post_image(post_id : str, credentials: HTTPAuthorizationCredentials = Security(security)):
    return Response(posts.get_file(post_id))

@router.delete("/",response_description="Delete post")
def delete_post(post_id:str,credentials: HTTPAuthorizationCredentials = Security(security)):
    user = users.get_current_user(credentials.credentials)
    posts.delete(post_id,user["_id"])

@router.get("/feed", response_description="Feed",response_model=List[Post])
def get_feed(credentials: HTTPAuthorizationCredentials = Security(security)):
    user = users.get_current_user(credentials.credentials)
    return posts.get_feed(user["_id"])
