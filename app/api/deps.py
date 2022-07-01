from typing import Generator

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
import jwt

from app.models.db import SessionLocal
from app.core.config import settings
from app import models
from app.core import security
from app.schemas import Token
from app.crud import get_user_by_email
from app.schemas import To

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_URL_PREFIX}/login/token'
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#
# def get_current_user(db: Session = Depends(get_db),
#                      token: str = Depends(oauth_scheme)) -> models.User:
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY,
#                    algorithms=[security.ALGORITHM])
#         token_data = To
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=404, detail='User does not exist')
#     user =