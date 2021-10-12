from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from loguru import logger
from starlette import status
from app.database.mongodb import db
from app.schemas.user import UserForm

collection_name = "users"


async def get_user(username: str):
    user = await db[collection_name].find_one({"username": username})
    return user


async def save_user(user: UserForm):
    logger.debug(db)
    if (await db[collection_name].find_one({"username": user.username})) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists!")

    user = jsonable_encoder(user)
    new_user = await db[collection_name].insert_one(user)
    created_user = await db[collection_name].find_one({"_id": new_user.inserted_id})
    return created_user
