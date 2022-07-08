from datetime import timedelta
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash, verify_password
from app import models, schemas


async def get_user_by_id(
        db: AsyncSession,
        id: int
) -> models.User:
    query = select(models.User).filter(models.User.id == id)
    q = await db.execute(query)
    return q.scalars().first()


async def get_users(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> List[models.User]:
    query = select(models.User).offset(skip).limit(limit).order_by(models.User.id)
    q = await db.execute(query)
    return q.scalars().all()


async def get_user_by_email(
        db: AsyncSession,
        email: str
) -> models.User:
    query = select(models.User).filter(models.User.email == email)
    q = await db.execute(query)
    return q.scalars().first()


async def create_user(
        db: AsyncSession,
        user_in: schemas.UserCreate
) -> models.User:
    db_user = models.User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate(
        db: AsyncSession,
        email: str,
        password: str
) -> Optional[models.User]:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
