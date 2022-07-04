from datetime import timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app import models, schemas
from app.core import security


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    db_user = models.User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate(db: Session,
                 email: str,
                 password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
