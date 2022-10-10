from fastapi import APIRouter, Body, Request, Response, HTTPException, status, File, UploadFile
from typing import List
from repositories.user import get_all_users, create_user, get_file_id
from models.user import User, UserIn

# from pymongo import ReturnDocument
# from fastapi.responses import JSONResponse, FileResponse

router = APIRouter()

@router.get("/", response_description="List all users", response_model=List[User])
def list_users(request: Request, limit : int = 100, skip : int = 0):
    return get_all_users(request.app.database, limit=limit, skip=skip)

@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=User)
def create(request : Request, user: UserIn = Body(...)):
    return create_user(request.app.database, user)

@router.post("/{user_id}", response_description="Set a new profile image")
def upload_file(request : Request, user_id : str, file: bytes = File()):
    file_id = get_file_id(request.app.database, file)
    request.app.database["users"].find_one_and_update({'_id': user_id},
                        { '$set': { "profile_image" : file_id} },
                        ) 