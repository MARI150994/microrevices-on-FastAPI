from typing import Optional, List, Union

from pydantic import BaseModel, EmailStr


class TokenBase(BaseModel):
    token: str


class TokenCreate(TokenBase):
    user_id: int


# Return to client
class Token(TokenBase):

    class Config:
        orm_mode = True
