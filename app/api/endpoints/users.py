from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
def read_users(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(get_db),
        user_in: schemas.UserCreate,
):
    user = crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='User with such email already exist'
        )
    user = crud.create_user(db, user_in)
    return user
