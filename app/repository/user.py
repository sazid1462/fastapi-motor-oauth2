from app.models.user import UserInDB
from app.database.fake_db import fake_users_db as db


def get_user(username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
