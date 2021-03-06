from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from loguru import logger

from app.core.config import settings
from app.core.security.auth import verify_token
from app.schemas.user import User
from app.repository.user import get_user
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/create")


async def __get_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await __get_user(token)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def verify_refresh_token(refresh_token: str = Header(None)):
    return await __get_user(refresh_token)
