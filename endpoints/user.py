from fastapi import APIRouter, Body, status, File
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
    _ = users.get_file_id(file)

@router.put("/{user_id}/name_surname", response_description="Update name and surname", response_model=User)
def update_name_and_surname(user_id : str, name : str, surname : str):
    return users.update_name_surname(user_id, name, surname)

@router.put("/{user_id}/username", response_description="Update username", response_model=User)
def update_user_username(user_id : str, username : str):
    return users.update_username(user_id, username)


'''
@router.post("/upload", response_description="test", response_model=str)
def test_upload(request : Request, file : bytes = File()):
    test = gridfs.GridFS(request.app.database)
    obj = test.put(file)
    return str(test.get(obj)._id)

@router.get("/upload", response_description="test")
def test_get(request : Request, file_id : str):
    test = gridfs.GridFS(request.app.database, "imgs_profile")
    if test.exists(ObjectId(file_id)):
        test.delete(ObjectId(file_id))
    raise "Err"
'''