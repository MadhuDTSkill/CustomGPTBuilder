from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional


# Schema for user registration
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# Schema for user login
class UserLogin(BaseModel):
    username: str
    password: str


# Schema for returning user data
class UserOut(BaseModel):
    uuid: UUID4
    username: str
    email: str

    class Config:
        orm_mode = True  # Enable ORM compatibility with SQLAlchemy models


# Schema for tokens
class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str

class LoginResponse(BaseModel):
    access : str
    refresh : str

# Schema for token data
class TokenData(BaseModel):
    username: Optional[str] = None
