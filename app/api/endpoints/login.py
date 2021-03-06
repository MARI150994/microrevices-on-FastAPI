from datetime import timedelta
from typing import Optional, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud
from app.api.deps import get_db
from app.core import security
from app.models import User
from app.api.deps import get_current_user
from app.cache import r


router = APIRouter()


# Create/return token for user (if it exists)
@router.post('/login/token', response_model=schemas.Token)
async def login_token(
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    # check if user exists and password correct
    user = await crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400,
                            detail='Incorrect email or password')
    token = security.create_token(subject=user.id)
    # add in cache
    await r.set(token, int(user.is_admin))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }


@router.post('/login/me', response_model=schemas.User)
async def test_token(current_user: User = Depends(get_current_user)):
    return current_user


# TODO call by RabbitMQ
# return user is admin or not
@router.post('/login/perm')
async def check_perm(current_user: User = Depends(get_current_user)):
    return current_user.is_admin
