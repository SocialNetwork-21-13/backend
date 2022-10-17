from fastapi import Body, Depends, FastAPI, APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from core.auth import Auth
from models.user import AuthModel, User
from repositories.user import UserRepository

router = APIRouter()

security = HTTPBearer()
auth_handler = Auth()

users = UserRepository()

@router.post('/signup', response_model=User)
def signup(user_details: AuthModel = Depends()):
    return users.signup(user_details.username, user_details.password)

@router.post('/login')
def login(user_details: AuthModel = Depends()):
    user = users.login(user_details.username, user_details.password)
    access_token = auth_handler.encode_token(user['username'])
    refresh_token = auth_handler.encode_refresh_token(user['username'])
    return {'access_token': access_token, 'refresh_token': refresh_token}

@router.get('/refresh_token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}

@router.get('/secret')
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if(auth_handler.decode_token(token)):
        return 'Top Secret data only authorized users can access this info'

@router.get("/user", response_model=User)
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    return users.get_current_user(credentials.credentials)