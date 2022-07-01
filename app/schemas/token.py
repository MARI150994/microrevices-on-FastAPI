from typing import Optional, List, Union

from pydantic import BaseModel, EmailStr


class TokenBase(BaseModel):
    token: str


class TokenCreate(TokenBase):
    user:

class TokenData(BaseModel):
    user_id: Optional[int] = None

