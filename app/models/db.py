import asyncio
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.config import settings

PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") \
              or settings.SQLALCHEMY_PG_CONN_URI

engine = create_async_engine(PG_CONN_URI, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False,
#                             bind=engine)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
