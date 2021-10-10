from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.repository.user import get_user

from ..dependencies import get_current_active_user

router = APIRouter()


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
