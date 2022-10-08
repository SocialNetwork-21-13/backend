from fastapi import APIRouter, Body, Request, Response, HTTPException, status,Depends
from fastapi.encoders import jsonable_encoder
from typing import List

from requests import request

from repositories.user import get_all, create
from models.user import User, UserIn

router = APIRouter()

''' 
@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=UserIn)
def create_user(request: Request, user: UserIn = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database["users"].insert_one(user)
    created_user = request.app.database["users"].find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user
'''

@router.get("/", response_description="List all users", response_model=List[User])
def list_users(request: Request, limit : int = 100, skip : int = 0):
    return get_all(request.app.database, limit=limit, skip=skip)

@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=UserIn)
def create_user(request : Request, user: UserIn = Body(...)):
    return create(request.app.database, user)