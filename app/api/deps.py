from datetime import timedelta
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.core import security
from app.models.db import async_session
from app.core.config import settings
from app import models, schemas, crud

oauth_scheme = OAuth2PasswordBearer(
    tokenUrl=f'/login/token'
)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_current_user(
        db: AsyncSession = Depends(get_db), token: str = Depends(oauth_scheme)
) -> models.User:
    try:
        print('TOKEN', token)
        token_payload = jwt.decode(jwt=token, key=settings.SECRET_KEY,
                                   algorithms=[security.ALGORITHM])
        print('TOKEN PAYLOAD', token_payload)
        token_data = schemas.TokenPayload(**token_payload)
    except (jwt.PyJWTError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token'
        )
    user = await crud.get_user_by_id(db, id=token_data.sender)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    return user

