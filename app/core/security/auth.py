from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from app.core.security.pass_util import verify_password

from app.repository.user import get_user
from app.core.config import settings
from app.schemas.user import User
from loguru import logger


async def authenticate_user(username: str, password: str):
    user = await get_user(username)

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_access_token(data: dict):
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    return create_jwt_token(data, access_token_expires)


def create_refresh_token(data: dict):
    refresh_token_expires = timedelta(
        minutes=settings.refresh_token_expire_minutes)
    return create_jwt_token(data, refresh_token_expires)


def create_tokens(user: User):
    access_token = create_access_token(
        data={"sub": user.username, "name": user.full_name,
              "role": user.role, "image": user.profile_photo}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "name": user.full_name,
              "role": user.role, "image": user.profile_photo}
    )
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


def verify_token(token: str):
    return jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
