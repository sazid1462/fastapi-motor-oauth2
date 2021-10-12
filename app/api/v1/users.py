from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.param_functions import Body
from app.schemas.user import User, UserForm
from app.repository.user import get_user, save_user

from ..dependencies import get_current_active_user

router = APIRouter()


@router.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserForm = Body(...)):
    saved_user = await save_user(user)
    return saved_user


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
