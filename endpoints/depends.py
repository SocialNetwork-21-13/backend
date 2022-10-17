from fastapi import Depends, HTTPException, status
from repositories.user import UserRepository
from core.security import JWTBearer, decode_access_token
from models.user import User

users = UserRepository()

async def get_current_user(
    token: str = Depends(JWTBearer()),
) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception
    username: str = payload.get("sub")
    if username is None:
        raise cred_exception
    user = users.get_by_username(username)
    if user is None:
        return cred_exception
    return user