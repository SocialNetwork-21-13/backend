from fastapi import APIRouter, Body, status,Response, File, UploadFile, Form, Depends
from typing import List
from repositories.post import PostRepository
from models.post import Post, PostIn

router = APIRouter()

posts = PostRepository()

@router.post("/{user_id}", response_description="Create a new post", status_code=status.HTTP_201_CREATED,response_model=Post)
def create(user_id,file: UploadFile=File(),post:PostIn=Depends()):
    file_id=posts.get_file_id(file.file)
    return posts.create(user_id,file_id, post)

@router.get("/", response_description="List all posts", response_model=List[Post])
def list_posts(limit : int = 100, skip : int = 0):
    return posts.get_all(limit=limit, skip=skip)

@router.put("/{user_id}/post_image", response_description="Set a new post image")
def upload_file(user_id : str, file: bytes = File()):
    file_id = posts.get_file_id(file)
    return posts.set_post_image(user_id, file_id)

@router.get("/{user_id}/get_post_image", response_description="Get post image")
def get_post_image(post_id : str):
    return Response(posts.get_file(post_id))

@router.delete("/{post_id}",response_description="Delete post")
def delete_post(post_id:str):
    posts.delete(post_id)