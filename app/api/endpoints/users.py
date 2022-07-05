from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, crud
from app.api.deps import get_db

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
async def read_users(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
async def create_user(
        *,
        db: AsyncSession = Depends(get_db),
        user_in: schemas.UserCreate,
):
    user = await crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='User with such email already exist'
        )
    user = await crud.create_user(db, user_in)
    return user
