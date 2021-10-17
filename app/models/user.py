from pydantic import Field
from app.schemas.user import User


class UserModel(User):
    password: str = Field(...)
    role: str = Field(...)
