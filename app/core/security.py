from datetime import timedelta, datetime

from passlib.context import CryptContext
import jwt


from app.core.config import settings

sec_context = CryptContext(schemes=['sha256_crypt'])


def get_password_hash(password: str) -> str:
    return sec_context.hash(password)


def verify_password(password_in: str, hashed_password: str) -> bool:
    return sec_context.verify(password_in, hashed_password)


ALGORITHM = "HS256"


def create_token(subject: str, expires: timedelta) -> str:
    if expires:
        expire_date = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=10
        )
    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
