from datetime import timedelta
from typing import Optional, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import get_db
from app.models import User, Token
from app.api.deps import get_current_user


router = APIRouter()


# Create/return token for user (if it exists)
@router.post('/login/token', response_model=schemas.Token)
def login_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    print('IN LOGIN TOKEN ENDPOINTS')
    # check if user exists and password correct
    user = crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400,
                            detail='Incorrect email or password')
    token: Token = crud.create_token(db, user_id=user.id)
    return token


@router.post('/login/me', response_model=schemas.User)
def test_token(current_user: User = Depends(get_current_user)):
    return current_user
