from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean(), default=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    token = relationship('Token', uselist=False, back_populates='user')


class Token(Base):
    token = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', uselist=False, back_populates='token')
