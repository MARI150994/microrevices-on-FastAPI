from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# TODO
# from app.core.config import settings

# TODO
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5432/network"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                            bind=engine)