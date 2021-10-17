from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

from pydantic.networks import EmailStr

from app.models.object_id import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    role: str = Field(...)
    profile_photo: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserForm(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
