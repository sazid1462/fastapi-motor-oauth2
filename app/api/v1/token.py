from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependencies import verify_refresh_token

from app.schemas.token import Token

from app.core.security.auth import authenticate_user, create_tokens
from app.schemas.user import User

router = APIRouter(prefix="/api/v1/token")


@router.post("/create", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_tokens(user)


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(verify_refresh_token)):
    return create_tokens(current_user)
