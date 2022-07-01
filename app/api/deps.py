from typing import Generator

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
import jwt

from app.models.db import SessionLocal
from app.core.config import settings
from app import models
from app.crud import get_user_by_token

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl=f'/login/token'
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(oauth_scheme)
) -> models.User:
    user = get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=404, detail={'Invalid token'})
    return user
