from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud
from app.models import User
from app.api.deps import get_db, get_current_user

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
async def read_users(
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
        skip: int = 0,
        limit: int = 100,
):
    if user.is_admin:
        users = await crud.get_users(db, skip=skip, limit=limit)
        return users
    raise HTTPException(status_code=403, detail='Not enough rights')


@router.post('/', response_model=schemas.User)
async def create_user(
        *,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
        user_in: schemas.UserCreate,
):
    if user.is_admin:
        user = await crud.get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail='User with such email already exist'
            )
        user = await crud.create_user(db, user_in)
        return user
    raise HTTPException(status_code=403, detail='Not enough rights')
