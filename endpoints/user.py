from fastapi import APIRouter, Body, status, File, Response
from typing import List
from repositories.user import UserRepository
from models.user import User, UserIn

# from pymongo import ReturnDocument
# from fastapi.responses import JSONResponse, FileResponse

router = APIRouter()

users = UserRepository()

@router.get("/", response_description="List all users", response_model=List[User])
def list_users(limit : int = 100, skip : int = 0):
    return users.get_all(limit=limit, skip=skip)

@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def create(user: UserIn = Body(...)):
    return users.create(user)

@router.put("/{user_id}/profile_image", response_description="Set a new profile image")
def upload_file(user_id : str, file: bytes = File()):
    file_id = users.get_file_id(file)
    return users.update_profile_image(user_id, file_id)

@router.post("/upload_default", response_description="Upload default image", status_code=status.HTTP_201_CREATED)
def upload_default_img(file : bytes = File()):
   users.upload_image(file)

@router.put("/{user_id}/name_surname", response_description="Update name and surname", response_model=User)
def update_name_and_surname(user_id : str, name : str, surname : str):
    return users.update_name_surname(user_id, name, surname)

@router.put("/{user_id}/username", response_description="Update username", response_model=User)
def update_user_username(user_id : str, username : str):
    return users.update_username(user_id, username)

@router.delete("/{user_id}", response_description="Delete account")
def delete_user(user_id : str):
    users.delete(user_id)

@router.get("/{user_id}/get_image", response_description="Get profile image")
def get_profile_image(user_id : str):
    return Response(users.get_file(user_id))

@router.put("/{user_id}/bio", response_description="Update bio", response_model=User)
def update_bio(user_id : str, bio : str):
    return users.update_bio(user_id, bio)