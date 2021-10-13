from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from loguru import logger
from starlette import status
from app.core.security.pass_util import get_password_hash
from app.database.mongodb import db
from app.models.user import UserModel
from app.schemas.user import UserForm

collection_name = "users"


async def get_user(username: str) -> UserModel:
    user = await db[collection_name].find_one({"username": username, "disabled": {"$ne": True}})
    if user is None:
        return None
    return UserModel(**user)


async def save_user(user: UserForm) -> UserModel:
    logger.debug(db)
    if (await db[collection_name].find_one({"username": user.username})) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists!")

    user.password = get_password_hash(user.password)
    user = jsonable_encoder(user)
    new_user = await db[collection_name].insert_one(user)
    created_user = await db[collection_name].find_one({"_id": new_user.inserted_id})
    return UserModel(**created_user)
