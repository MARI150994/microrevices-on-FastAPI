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


def create_token(
        subject: str,
        expires: timedelta = None
) -> str:
    if not expires:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expire = datetime.utcnow() + expires
    to_encode = {'exp': expire, 'sender': str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
