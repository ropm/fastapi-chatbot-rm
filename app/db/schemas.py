from typing import List, Optional

from pydantic import BaseModel, Json


class IntentBase(BaseModel):
    intents: Json
    description: Optional[str] = None

# print(IntentBase(intents='{"b": 1}'))
# > intents={'b': 1}


class IntentCreate(IntentBase):
    pass


class Intent(IntentBase):
    id: int


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    hashed_password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
