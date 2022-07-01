from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db
from app.core import security
from app.core.config import settings
from app.schemas import TokenData

router = APIRouter()


# Create token foe user if it exists
@router.post('/login/token', response_model=schemas.Token)
def login_token(db: Session = Depends(get_db),
                form_data: OAuth2PasswordRequestForm= Depends()):
    user = crud.authenticate(db, email=form_data.username,
                             password=form_data.password)
    if not user:
        raise HTTPException(status_code=400,
                            detail='Incorrect email or password')
    token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'token': security.create_token(user.id,
                                       expires=token_expires),
        'token type': 'Bearer',
    }
#
# @router.post('/login/me', response_model=schemas.User)
# def test_token(current_user: models.User = Depends(deps))